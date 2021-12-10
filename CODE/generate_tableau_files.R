# Import libraries
library(car)
library(MASS)
library(arrow) #for reading the parquet file
library(dplyr)
library(tidyr)
library(stringr)
library(data.table)


# load the data
tableauRawData = read_parquet(
  "generate_tableau_files.parquet",
  col_select = NULL,
  as_data_frame = TRUE
)
tableauRaw.row.cnt = nrow(tableauRawData)

# load the data
tableauPlayers <- read.csv("player_final.csv",header=TRUE)
playerVars <- c("DISPLAY_FIRST_LAST","TEAM_CITY","TEAM_ABBREVIATION","TEAM_NAME")
tableauPlayers <- tableauPlayers[playerVars]



########################################################
# create sum of the weighted true shooting and true shooting dif (for that matchup)
# (matchupts-offplayerts)*matchupmins
# a negative value means that the defensive player
# is holding the off player to a lower shooting pct
# than their norm, so it is better for the defensive
# player

tableauRawData$matchup_ts_diff <- (tableauRawData$matchup_ts) - tableauRawData$off_player_ts

tableauRawData$sum_ts_def <- (tableauRawData$matchup_ts)*tableauRawData$matchup_min

tableauRawData$sum_ts_off <- (tableauRawData$off_player_ts)*tableauRawData$matchup_min

tableauRawData$weighted_ts_diff <- tableauRawData$sum_ts_def - tableauRawData$sum_ts_off

tableauRawData$matchup_player_pts_pct_diff <- 100 * (tableauRawData$matchup_player_pts - tableauRawData$avg_matchup_player_pts) / tableauRawData$avg_matchup_player_pts

tableauRawData$matchup_team_pts_pct_diff <- 100 * (tableauRawData$matchup_team_pts - tableauRawData$avg_matchup_team_pts) / tableauRawData$avg_matchup_team_pts

tableauRawData$weighted_player_pts_pct_diff <- tableauRawData$matchup_min*tableauRawData$matchup_player_pts_pct_diff

tableauRawData$weighted_team_pts_pct_diff <- tableauRawData$matchup_min*tableauRawData$matchup_team_pts_pct_diff


##############################################

#############################################
# create the height and weight category columns
# create the df's for posn and height / position and weight
# in order to get the median values by position
select_vars_hgt <- c("off_player_pos","off_height")
select_vars_wgt <- c("off_player_pos","off_weight")
df_height <- tableauRawData[select_vars_hgt]
df_weight <- tableauRawData[select_vars_wgt]

# get the median hgt/wgt by position
df_hgt_med <- df_height%>%
  group_by(off_player_pos)%>% 
  summarise(Median=median(off_height))
df_wgt_med <- df_weight%>%
  group_by(off_player_pos)%>% 
  summarise(Median=median(off_weight))

# create height/weight category columns
tableauRawData['o_hgt_cat'] <- NA
tableauRawData['o_wgt_cat'] <- NA
tableauRawData['d_hgt_cat'] <- NA
tableauRawData['d_wgt_cat'] <- NA


# set the hgt/wgt categories by position
# in the raw data file
# height
for(i in 1:nrow(df_hgt_med)) {       # for-loop over rows
      posn <- df_hgt_med[i,]$off_player_pos
      val <- df_hgt_med[i,]$Median
      print(posn)
      print(val)

      tableauRawData$o_hgt_cat[tableauRawData$off_player_pos==posn & tableauRawData$off_height < val] <- "Short"  
      tableauRawData$o_hgt_cat[tableauRawData$off_player_pos==posn & tableauRawData$off_height >= val] <- "Tall"  
      tableauRawData$d_hgt_cat[tableauRawData$def_player_pos==posn & tableauRawData$def_height < val] <- "Short"  
      tableauRawData$d_hgt_cat[tableauRawData$def_player_pos==posn & tableauRawData$def_height >= val] <- "Tall"  

}

# weight
for(i in 1:nrow(df_wgt_med)) {       # for-loop over rows
  posn <- df_wgt_med[i,]$off_player_pos
  val <- df_wgt_med[i,]$Median
  print(posn)
  print(val)
  
  tableauRawData$o_wgt_cat[tableauRawData$off_player_pos==posn & tableauRawData$off_weight < val] <- "Light"  
  tableauRawData$o_wgt_cat[tableauRawData$off_player_pos==posn & tableauRawData$off_weight >= val] <- "Heavy"  
  tableauRawData$d_wgt_cat[tableauRawData$def_player_pos==posn & tableauRawData$def_weight < val] <- "Light"  
  tableauRawData$d_wgt_cat[tableauRawData$def_player_pos==posn & tableauRawData$def_weight >= val] <- "Heavy"  
  
}
############################################

############################################
# Add the team information for the offensive players
# to the matchups

tableauRawData <- merge(x = tableauRawData, y = tableauPlayers, 
                        by.x = "off_player_name", by.y = "DISPLAY_FIRST_LAST", all.x=TRUE)  
# rename the team columns to be for offensive
names(tableauRawData)[names(tableauRawData) == 'TEAM_CITY'] <- 'off_team_city'
names(tableauRawData)[names(tableauRawData) == 'TEAM_ABBREVIATION'] <- 'off_team_abbr'
names(tableauRawData)[names(tableauRawData) == 'TEAM_NAME'] <- 'off_team_name'
# remove DISPLAY_FIRST_LAST
drop <- c("DISPLAY_FIRST_LAST")
tableauRawData = tableauRawData[,!(names(tableauRawData) %in% drop)]

# now do the same for the defensive players
# in the matchups
tableauRawData <- merge(x = tableauRawData, y = tableauPlayers, 
                        by.x = "def_player_name", by.y = "DISPLAY_FIRST_LAST", all.x=TRUE)  
# rename the team columns to be for offensive
names(tableauRawData)[names(tableauRawData) == 'TEAM_CITY'] <- 'def_team_city'
names(tableauRawData)[names(tableauRawData) == 'TEAM_ABBREVIATION'] <- 'def_team_abbr'
names(tableauRawData)[names(tableauRawData) == 'TEAM_NAME'] <- 'def_team_name'
# remove DISPLAY_FIRST_LAST
drop <- c("DISPLAY_FIRST_LAST")
tableauRawData = tableauRawData[,!(names(tableauRawData) %in% drop)]


############################################

############################################
# Add the player position and physical traits
# to the players data frame
tableauPlayersFinal <- merge(x = tableauPlayers, y = tableauRawData, 
                        by.y = "off_player_name", by.x = "DISPLAY_FIRST_LAST", all.x=TRUE) 

names(tableauPlayersFinal)[names(tableauPlayersFinal) == 'DISPLAY_FIRST_LAST'] <- 'player_name'
names(tableauPlayersFinal)[names(tableauPlayersFinal) == 'off_player_pos'] <- 'position'
names(tableauPlayersFinal)[names(tableauPlayersFinal) == 'off_height'] <- 'height'
names(tableauPlayersFinal)[names(tableauPlayersFinal) == 'o_hgt_cat'] <- 'hgt_cat'
names(tableauPlayersFinal)[names(tableauPlayersFinal) == 'off_weight'] <- 'weight'
names(tableauPlayersFinal)[names(tableauPlayersFinal) == 'o_wgt_cat'] <- 'wgt_cat'
names(tableauPlayersFinal)[names(tableauPlayersFinal) == 'off_team_city'] <- 'team_city'
names(tableauPlayersFinal)[names(tableauPlayersFinal) == 'off_team_abbr'] <- 'team_abbr'
names(tableauPlayersFinal)[names(tableauPlayersFinal) == 'off_team_name'] <- 'team_name'
names(tableauPlayersFinal)[names(tableauPlayersFinal) == 'off_player_min'] <- 'player_min'
names(tableauPlayersFinal)[names(tableauPlayersFinal) == 'off_player_pts'] <- 'player_pts'
names(tableauPlayersFinal)[names(tableauPlayersFinal) == 'off_player_ts'] <- 'player_ts'

# select the columns to keep and write the csv file
playerFinalVars <- c('player_name','position','height','hgt_cat',
                     'weight','wgt_cat','team_city','team_abbr',
                     'team_name','player_min','player_pts','player_ts')
tableauPlayersFinal <- tableauPlayersFinal[playerFinalVars]

# keep only the distinct values.
tableauPlayersFinal <- unique(tableauPlayersFinal, by = playerFinalVars)
tableauPlayersFinal <- tableauPlayersFinal %>% drop_na(position)

#write the tableau file
write.csv(tableauPlayersFinal,"tableauPlayers.csv")

##########################################################


# create the ungrouped Tableau data frame
# and export to Tableau data file
select_vars <- c("def_player_name","def_height","d_hgt_cat","def_weight","d_wgt_cat",
                 "off_player_name","off_height","o_hgt_cat","off_weight","o_wgt_cat",
                 "off_player_pos","def_player_pos",
                 "off_team_city","off_team_abbr","off_team_name",
                 "def_team_city","def_team_abbr","def_team_name",
                 "matchup_min","matchup_ts","off_player_ts","matchup_ts_diff","weighted_ts_diff",
                 "matchup_player_pts_pct_diff", "weighted_player_pts_pct_diff",
                 "matchup_team_pts_pct_diff", "weighted_team_pts_pct_diff")
tableauData_ungrouped <- tableauRawData[select_vars]



write.csv(tableauData_ungrouped,"tableauData_detail.csv")
############################################

############################################
# create the defensive player summary Tableau data frame
# and export to Tableau data file
select_vars2 <- c("def_player_name","def_height","d_hgt_cat","def_weight","d_wgt_cat",
                 "o_hgt_cat","o_wgt_cat","off_player_pos","def_player_pos",
                 "def_team_city","def_team_abbr","def_team_name",
                 "matchup_min","matchup_ts","off_player_ts","matchup_ts_diff","weighted_ts_diff",
                 "matchup_player_pts_pct_diff", "weighted_player_pts_pct_diff",
                 "matchup_team_pts_pct_diff", "weighted_team_pts_pct_diff")
tableauData_def_player_summary <- tableauRawData[select_vars2]

grp1 <- c("def_player_name","def_height","d_hgt_cat","def_weight","d_wgt_cat",
          "def_team_city","def_team_abbr","def_team_name",
         "o_hgt_cat","o_wgt_cat","off_player_pos","def_player_pos")
tableauData_def_player_grouped <- tableauData_def_player_summary %>%
  group_by(across(all_of(grp1))) %>% 
  summarize(avg_ts_diff = sum(weighted_ts_diff)/sum(matchup_min),
            sum_matchup_min=sum(matchup_min),
            sum_ts_diff=sum(weighted_ts_diff),
            avg_player_pts_pct_diff=sum(weighted_player_pts_pct_diff)/sum(matchup_min),
            sum_player_pts_pct_diff=sum(weighted_player_pts_pct_diff),
            avg_team_pts_pct_diff=sum(weighted_team_pts_pct_diff)/sum(matchup_min),
            sum_team_pts_pct_diff=sum(weighted_team_pts_pct_diff)
  )



write.csv(tableauData_def_player_grouped,"tableauData_def_player_grouped.csv")

############################################


############################################
# create the offensive player summary Tableau data frame
# and export to Tableau data file
select_vars3 <- c("off_player_name","off_height","o_hgt_cat","off_weight","o_wgt_cat",
                  "d_hgt_cat","d_wgt_cat","off_player_pos","def_player_pos",
                  "off_team_city","off_team_abbr","off_team_name",
                  "matchup_min","matchup_ts","off_player_ts","matchup_ts_diff","weighted_ts_diff",
                  "matchup_player_pts_pct_diff", "weighted_player_pts_pct_diff",
                  "matchup_team_pts_pct_diff", "weighted_team_pts_pct_diff"
                  )
tableauData_off_player_summary <- tableauRawData[select_vars3]

grp2 <- c("off_player_name","off_height","o_hgt_cat","off_weight","o_wgt_cat",
          "off_team_city","off_team_abbr","off_team_name",
          "d_hgt_cat","d_wgt_cat","off_player_pos","def_player_pos")
tableauData_off_player_grouped <- tableauData_off_player_summary %>%
  group_by(across(all_of(grp2))) %>% 
  summarize(avg_ts_diff = sum(weighted_ts_diff)/sum(matchup_min),
            sum_matchup_min=sum(matchup_min),
            sum_ts_diff=sum(weighted_ts_diff),
            avg_player_pts_pct_diff=sum(weighted_player_pts_pct_diff)/sum(matchup_min),
            sum_player_pts_pct_diff=sum(weighted_player_pts_pct_diff),
            avg_team_pts_pct_diff=sum(weighted_team_pts_pct_diff)/sum(matchup_min),
            sum_team_pts_pct_diff=sum(weighted_team_pts_pct_diff)
            )


write.csv(tableauData_off_player_grouped,"tableauData_off_player_grouped.csv")

############################################


############################################
# create the overall summary Tableau data frame
# and export to Tableau data file
select_vars3 <- c("d_hgt_cat","d_wgt_cat",
                  "o_hgt_cat","o_wgt_cat","off_player_pos","def_player_pos",
                  "matchup_min","matchup_ts","off_player_ts","matchup_ts_diff","weighted_ts_diff",
                  "matchup_player_pts_pct_diff", "weighted_player_pts_pct_diff",
                  "matchup_team_pts_pct_diff", "weighted_team_pts_pct_diff"
                  )
tableauData_overall_summary <- tableauRawData[select_vars3]

grp3 <- c("d_hgt_cat","d_wgt_cat",
          "o_hgt_cat","o_wgt_cat","off_player_pos","def_player_pos")
tableauData_overall_grouped <- tableauData_overall_summary %>%
  group_by(across(all_of(grp3))) %>% 
  summarize(avg_ts_diff = sum(weighted_ts_diff)/sum(matchup_min),
            sum_matchup_min=sum(matchup_min),
            sum_ts_diff=sum(weighted_ts_diff),
            avg_player_pts_pct_diff=sum(weighted_player_pts_pct_diff)/sum(matchup_min),
            sum_player_pts_pct_diff=sum(weighted_player_pts_pct_diff),
            avg_team_pts_pct_diff=sum(weighted_team_pts_pct_diff)/sum(matchup_min),
            sum_team_pts_pct_diff=sum(weighted_team_pts_pct_diff)
            )

write.csv(tableauData_overall_grouped,"tableauData_overall_grouped.csv")

############################################

############################################
# create the overall summary Tableau data frame
# grouped only by offensive and defensive position
# and export to Tableau data file
select_vars4 <- c("off_player_pos","def_player_pos",
                  "matchup_min","matchup_ts","off_player_ts","matchup_ts_diff","weighted_ts_diff",
                  "matchup_player_pts_pct_diff", "weighted_player_pts_pct_diff",
                  "matchup_team_pts_pct_diff", "weighted_team_pts_pct_diff"
                  )
tableauData_position_summary <- tableauRawData[select_vars4]

grp4 <- c("off_player_pos","def_player_pos")
tableauData_overall_position_grouped <- tableauData_position_summary %>%
  group_by(across(all_of(grp4))) %>% 
  summarize(avg_ts_diff = sum(weighted_ts_diff)/sum(matchup_min),
            sum_matchup_min=sum(matchup_min),
            sum_ts_diff=sum(weighted_ts_diff),
            avg_player_pts_pct_diff=sum(weighted_player_pts_pct_diff)/sum(matchup_min),
            sum_player_pts_pct_diff=sum(weighted_player_pts_pct_diff),
            avg_team_pts_pct_diff=sum(weighted_team_pts_pct_diff)/sum(matchup_min),
            sum_team_pts_pct_diff=sum(weighted_team_pts_pct_diff)
            
            )

write.csv(tableauData_overall_position_grouped,"tableauData_overall_position_grouped.csv")

############################################











