if [ -f $1 ]; then
    sed -i  's/\s$//g' $1
    sed -i -E 's/^\s+$//g' $1; 
else
    echo "Fichero $1 es inválido"
fi
