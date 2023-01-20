
library(FactoMineR)

#import du fichier
df <- read.csv("analyse_score_etic.csv", sep=";", na.strings="")


# afficher les colonnes possibles
colnames(df)


# afficher les 6 premires lignes
head(df)

# supprimer les lignes contenant des valeurs manquantes
df <- na.omit(df)

sum(is.na(df))

df <- df[, -c("Code_UAI", "postesinfoelvhorscours", "terminaux_num")]

# commencer à faire l'ACM
acm <- MCA(df)


dimdesc(acm)
