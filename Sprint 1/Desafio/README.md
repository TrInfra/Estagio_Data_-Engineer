# Criação do diretório de backup
mkdir -p vendas/backup

# Mensagem informativa
echo "O Script está em execução. Aguarde a finalização."

# Copia o arquivo de vendas para o diretório vendas
cp /home/nycolasdev/ecommerce/dados_de_vendas.csv /home/nycolasdev/ecommerce/vendas/

# Navega até o diretório vendas
cd /home/nycolasdev/ecommerce/vendas/

# Cria uma cópia do arquivo de vendas no diretório de backup
cp /home/nycolasdev/ecommerce/vendas/dados_de_vendas.csv /home/nycolasdev/ecommerce/vendas/backup/

# Renomeia o arquivo de vendas no diretório de backup com a data atual
cd /home/nycolasdev/ecommerce/vendas/backup/
mv dados_de_vendas.csv dados-$(date +%Y%m%d).csv

# Renomeia todos os arquivos CSV no diretório de backup com o prefixo "backup-"
for files in *.csv; do
  mv "$files" "backup-$files"
done

# Adiciona a data do relatório ao arquivo relatorio.txt
echo "Data do relatório: $(date +'%Y %m-%d %H:%M')" >> relatorio.txt

# Encontra o arquivo de backup com a data atual
Encontrar_data_atual=$(date +%Y%m%d)
Arq_dataAtual=$(find . -type f -name "backup-dados-${Encontrar_data_atual}.csv")

# Obtém a data do primeiro produto vendido
first_produtoDATA=$(awk -F',' 'NR>1{split($5, date, "/"); printf "%s,%s\n", date[3] "/" date[2] "/" date[1], $0}' $Arq_dataAtual | sort -t',' -k1,1 | cut -d',' -f6 | head -n 1)
echo "Data do primeiro produto vendido: $first_produtoDATA" >> relatorio.txt

# Obtém a data do último produto vendido
last_produtoDATA=$(awk -F',' 'NR>1{split($5, date, "/"); printf "%s,%s\n", date[3] "/" date[2] "/" date[1], $0}' $Arq_dataAtual | sort -t',' -k1,1 | cut -d',' -f6 | tail -n 1)
echo "Data do último produto vendido: $last_produtoDATA" >> relatorio.txt

# Calcula a quantidade de itens diferentes no arquivo de backup
echo "Quantidade de itens diferentes: $(awk -F "," 'END {print NR-1}' "$Arq_dataAtual")" >> relatorio.txt

# Adiciona os 10 primeiros itens vendidos ao arquivo relatorio.txt
echo "Os 10 primeiros itens vendidos:" >> relatorio.txt
head -n10 $Arq_dataAtual >> relatorio.txt
echo "" >> relatorio.txt
echo "" >> relatorio.txt
echo "" >> relatorio.txt

# Compacta o arquivo de backup com a data atual
zip backup-dados-${Encontrar_data_atual}.zip ${Arq_dataAtual}

# Remove o arquivo original de vendas
rm ${Arq_dataAtual}

# Volta ao diretório principal
cd ..

# Remove o arquivo original de vendas (dados_de_vendas.csv)
rm dados_de_vendas.csv

# Mensagem de conclusão
echo "Finalizando o Script ..."


# Etapas


1. ...
[Etapa I](etapa-1/entrega.txt)


2. ...
[Etapa II](etapa-2/entrega.txt)




