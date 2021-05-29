library("geosphere")
df = read.csv('data/weather_features.csv')
dates = substr(df$Datetime, 1, 10)
daylengths = list()
for (date in dates){
tmp <- daylength(55.56, date)
daylengths[[date]] = tmp
}
write.csv(daylengths, "data/daylengths.csv", row.names = TRUE)

