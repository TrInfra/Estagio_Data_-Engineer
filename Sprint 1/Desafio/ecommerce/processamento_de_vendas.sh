#!/bin/bash
mkdir -p vendas/backup
echo "O Script Está em execução aguarde a finalização"
cp /home/nycolasdev/ecommerce/dados_de_vendas.csv /home/nycolasdev/ecommerce/vendas/
cd /home/nycolasdev/ecommerce/vendas/
cp /home/nycolasdev/ecommerce/vendas/dados_de_vendas.csv /home/nycolasdev/ecommerce/vendas/backup/

cd /home/nycolasdev/ecommerce/vendas/backup/
mv dados_de_vendas.csv dados-$(date +%Y%m%d).csv
for files in *.csv; do
mv "$files" "backup-$files"
done


echo "Data do relatório: $(date +'%Y %m-%d %H:%M')" >> relatorio.txt
Encontrar_data_atual=$(date +%Y%m%d)
Arq_dataAtual=$(find . -type f -name "backup-dados-${Encontrar_data_atual}.csv")


first_produtoDATA=$(awk -F',' 'NR>1{split($5, date, "/"); printf "%s,%s\n", date[3] "/" date[2] "/" date[1], $0}' $Arq_dataAtual | sort -t',' -k1,1 | cut -d',' -f6 | head -n 1)
echo "Data do primeiro produto vendido: $first_produtoDATA" >> relatorio.txt

last_produtoDATA=$(awk -F',' 'NR>1{split($5, date, "/"); printf "%s,%s\n", date[3] "/" date[2] "/" date[1], $0}' $Arq_dataAtual | sort -t',' -k1,1 | cut -d',' -f6 | tail -n 1)
echo "Data do ultimo produto vendido: $last_produtoDATA" >> relatorio.txt




echo "Quantidade de itens diferentes: $(awk -F "," 'END {print NR-1}' "$Arq_dataAtual")" >> relatorio.txt
echo "Os 10 primeiros itens vendidos:" >> relatorio.txt
head -n10 $Arq_dataAtual >> relatorio.txt
echo "" >> relatorio.txt
echo "" >> relatorio.txt
echo "" >> relatorio.txt
zip backup-dados-${Encontrar_data_atual}.zip ${Arq_dataAtual}
rm ${Arq_dataAtual}

cd ..
rm dados_de_vendas.csv

echo "Finalizando o Script ..."
