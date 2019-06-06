for file in *.JPG
do
  mv "$file" "New_N_${file%.JPG}.png"
done
