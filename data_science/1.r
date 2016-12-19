# encode:UTF-8
# -----------------------問題１-------------------------- #
cat("\n\n\n", "1. Factor型のベクトルをアルファベット順に並べ替えてください")

a <- factor(c("beta","sigma","phi","alpha"))
cat("\n", "vector:", a)
cat("\n", "sort(vector): ", sort(a))


# -----------------------問題２-------------------------- #
cat("\n\n\n", "2. データフレームの25歳以下の行を取り出してください")

a <- data.frame(name=c("tanaka","satou","suzuki","oda"), age=c(22,25,27,25), status=c("normal","normal","normal","unusual"))

cat("\n", "dataframe: ", "\n")
print(a)

cat("\n", "25 ages in dataframe: ", "\n")
print(a[a$age==25,])

# -----------------------問題３-------------------------- #
cat("\n\n\n", "3. リストの中にリストを作ってください")

# ------------------------------- #
cat("\n\n", "3-1 tag付きのリスト")
a <- list(name = "yoshino", age = 18, status = "normal")

cat("\n", "list: ", "\n")
print(a)

a$status = list(body = "normal", mind = "normal")
cat("\n", "edited list: ", "\n")
print(a)
# ------------------------------- #
cat("\n\n", "3-2 ta付いてないリスト")
a <- list(10,20,30)

cat("\n", "list: ")
print(a)

a[[1]] <- list(10,11,12,13)
cat("\n", "edited list: ")
print(a)

# -----------------------問題４-------------------------- #
cat("\n\n\n 4. ディレクトリの中のCSVファイルすべてのファイル名の拡張子.csvを、.txtに変換して表示してください. \n\n")

cat("ソースコードに、下のFALSEをTRUEに変わると、コード4-1が実行する")
if(FALSE){
# ------------------------------- #
cat("\n\n", "4-1 forループを使う \n")
# ファイル名をリスト形で読み込み -> for リスト全てのメンバー -> 尾の".csv"を切り落とす -> ".txt"を尾に付ける
csv_files <- list.files(pattern=".csv")
for (name_csv in csv_files) {
  name_txt <- (paste(strsplit(name_csv,".csv")[1], ".txt", sep=""))
  file.rename( name_csv, name_txt )
  cat(name_csv, "を", name_txt, "に変わりました \n")
}
}　
# end if

#　下のFALSEをTRUEに変わるとコード4-2が実行する
if(FALSE){
# ------------------------------- #
cat("\n\n", "4-2 lapplyまたはsapplyを使う \n")

csv_for_txt <- function(name_csv){
  name_txt <- paste(strsplit(name_csv,".csv")[1], ".txt", sep="")
  file.rename(name_csv, name_txt)
  cat(name_csv, "を", name_txt, "に変わりました \n")
}

csv_files <- list.files(pattern=".csv")
sapply(csv_files, csv_for_txt)

}　
# end if
# -----------------------問題５-------------------------- #
cat("\n\n\n", "5. 引数1を渡すと グー、2を渡すとチョキ、何も渡さないとパーを表示する関数を作れ ")
finger_guessing <- function(x=3){
  cat("\n", "get:", x,"  finger is: ")
  if (x==1) cat("グー")
  else  if(x==2) cat("チョキ")
        else cat("パー")
  cat("\n")
}

finger_guessing(a <- 1)
finger_guessing(a <- 2)
finger_guessing(a <- 3)
finger_guessing(a <- "a")
finger_guessing(a <- 32769)
finger_guessing(a <- "日本語わかる？")


# -----------------------問題６-------------------------- #
cat("\n\n\n", "6. 平均50, 標準偏差10の正規分布に従う乱数のヒストグラムをプロットせよ")

sample_num <- 500
hist(rnorm(sample_num,50,10))
