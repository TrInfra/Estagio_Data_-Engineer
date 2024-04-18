# __#Etapas__
Para realizar com êxito os passos abaixo, baixe antes no seu terminal linux as ferramenta Cron e o editor de texto nano _(ou qualquer editor de texto de sua preferência)._  

#### Terminal
```bash
    sudo apt install cron   
    sudo apt install nano
```

## _Etapa 1_
### No linux crie um diretório chamado de ecommerce, siga os seguintes passos:
#### abra o terminal e digite:  
```bash
    mkdir /home/nycolasdev/ecommerce/  
    cd /home/nycolasdev/ecommerce/
```
#### **Não esqueça de substituir "nycolasdev" pelo seu nome de usuário.**
## _Etapa 2_
### Criar um arquivo chamado processamento_de_vendas.sh
#### No terminal:
```bash
    touch processamento_de_dados.sh
    nano processamento_de_dados.sh
```
### _Dentro de processamento_de_vendas.sh siga esses passos:_
#### processamento_de_vendas.sh no editor de texto
```bash
    #!/bin/bash  --> especificar qual interpretador de comandos deve ser usado para executar o script. 
    cd /home/nycolasdev/ecommerce/ 
    mkdir -p vendas/backup 
    #Criação do diretório de vendas e backup

    echo "O Script está em execução. Aguarde a finalização." 
    #Mensagem informativa (não obrigatório)

    cp /home/nycolasdev/ecommerce/dados_de_vendas.csv /home/nycolasdev/ecommerce/vendas/ 
    #Copia o arquivo de dados_de_vendas.csv para o diretório vendas

    cd /home/nycolasdev/ecommerce/vendas/
    #Navegue até o diretório vendas
    
    cp /home/nycolasdev/ecommerce/vendas/dados_de_vendas.csv /home/nycolasdev/ecommerce/vendas/backup/
    #Cria uma cópia do arquivo de vendas no diretório de backup

    cd /home/nycolasdev/ecommerce/vendas/backup/

    mv dados_de_vendas.csv dados-$(date +%Y%m%d).csv
    #Renomeia o arquivo de vendas no diretório de backup com a data atual

    for files in *.csv; do
        mv "$files" "backup-$files"
    done
    #Renomeia todos os arquivos CSV no diretório de backup com o prefixo "backup-"

    echo "Data do relatório: $(date +'%Y %m-%d %H:%M')" >> relatorio.txt
    #Adiciona a data do relatório ao arquivo relatorio.txt

    Encontrar_data_atual=$(date +%Y%m%d)
    Arq_dataAtual=$(find . -type f -name "backup-dados-${Encontrar_data_atual}.csv")
    #Encontra o arquivo de backup com a data atual

    first_produtoDATA=$(awk -F',' 'NR>1{split($5, date, "/"); printf "%s,%s\n", date[3] "/" date[2] "/" date[1], $0}' $Arq_dataAtual | sort -t',' -k1,1 | cut -d',' -f6 | head -n 1)

    echo "Data do primeiro produto vendido: $first_produtoDATA" >> relatorio.txt
    # Obtém a data do primeiro produto vendido

    last_produtoDATA=$(awk -F',' 'NR>1{split($5, date, "/"); printf "%s,%s\n", date[3] "/" date [2] "/" date[1], $0}' $Arq_dataAtual | sort -t',' -k1,1 | cut -d',' -f6 | tail -n 1)

    echo "Data do último produto vendido: $last_produtoDATA" >> relatorio.txt
    # Obtém a data do último produto vendido

    echo "Quantidade de itens diferentes: $(awk -F "," 'END {print NR-1}' "$Arq_dataAtual")">> relatorio.txt
    # Calcula a quantidade de itens diferentes no arquivo de backup

    echo "Os 10 primeiros itens vendidos:" >> relatorio.txt
    head -n10 $Arq_dataAtual >> relatorio.txt
    # Adiciona os 10 primeiros itens vendidos ao arquivo relatorio.txt

    echo "" >> relatorio.txt
    echo "" >> relatorio.txt
    echo "" >> relatorio.txt

    zip backup-dados-${Encontrar_data_atual}.zip ${Arq_dataAtual}
    # Compacta o arquivo de backup com a data atual

    rm ${Arq_dataAtual}
    # Remove o arquivo original de vendas

    cd ..
    # Volta ao diretório vendas/

    rm dados_de_vendas.csv
    ## Remove o arquivo original de vendas (dados_de_vendas.csv)
    
```
### Não podemos esquecer de tranformar o arquivo em executável e dar as permissões de execução
####  Salve e feche o arquivo e abra o terminal e digite:  
```bash
    chmod +x /home/nycolasdev/ecommerce/processamento_de_vendas.sh 
```
## _Etapa 3_
### _Programar o arquivo para funcionar na data e hora específicada_
#### Terminal
```bash
    crontab -e   
```
Escolha o editor de texto de sua preferência e em seguida irá abrir esse editor, navegue até a última linha dele e digite o seguinte:
```bash
    27 15 * * 1-4 /home/nycolasdev/ecommerce/processamento_de_vendas.sh
      
    #os primeiros dois digitos representam os minutos e os outros dois representam as horas os  1-4 representam os dias da semana, no caso são de 0 a 7 em que (0,7) representam domingo, 1  representa segunda-feira e 4 quinta-feira   
```
Para confirmar se tudo ocorreu como o esperado digite o seguinte comando no terminal:
```bash
    crontab -l  
```
Deve aparecer algo como isso para você:
```bash
nycolasdev@nycolasdev-virtual-machine:~$ crontab -l
# Edit this file to introduce tasks to be run by cron.
# 
# Each task to run has to be defined through a single line
# indicating with different fields when the task will be run
# and what command to run for the task
# 
# To define the time you can provide concrete values for
# minute (m), hour (h), day of month (dom), month (mon),
# and day of week (dow) or use '*' in these fields (for 'any').
# 
# Notice that tasks will be started based on the cron's system
# daemon's notion of time and timezones.
# 
# Output of the crontab jobs (including errors) is sent through
# email to the user the crontab file belongs to (unless redirected).
# 
# For example, you can run a backup of all your user accounts
# at 5 a.m every week with:
# 0 5 * * 1 tar -zcf /var/backups/home.tgz /home/
# 
# For more information see the manual pages of crontab(5) and cron(8)
# 
# m h  dom mon dow   command
27 15 * * 1-4  /home/nycolasdev/ecommerce/processamento_de_vendas.sh

nycolasdev@nycolasdev-virtual-machine:~$ 
```
Se isso apareceu para você então tudo ocorreu como planejado.

#### Agora o próximo passo é criar um arquivo com o nome __consolidador_de_processamentos_de_vendas.sh__  que terá a função de concatenar os relatórios em um só relatório chamado de relatorio_fina.txt .
#### OBS: optei por criar relatorio.txt e relatorio_fina.txt fora do arquivo processamento_de_vendas.sh pois poderia ocorrer um erro de conflito com os arquivos sendo criados toda vez que o script for executado, então vou mostrar os passos corretos para criar separadamente do script esses dois arquivos e eles devem ser criados antes de executar o arquivo para prevenção de erros.
#### Terminal:
```bash
    cd /home/nycolasdev/ecommerce/vendas/backup
    touch relatorio.txt relatorio_fina.txt
```
#### Agora o podemos voltar para a criação do arquivo __consolidador_de_processamentos_de_vendas.sh__  .
#### Terminal:
```bash
    touch consolidador_de_processamentos_de_vendas.sh
    nano consolidador_de_processamentos_de_vendas.sh
```
### _Dentro de consolidador_de_processamentos_de_vendas.sh siga esses passos:_
#### consolidador_de_processamentos_de_vendas.sh no editor de texto
```bash
    #!/bin/bash
    cd /home/nycolasdev/ecommerce/vendas/backup/
    head -n 999999999 /home/nycolasdev/ecommerce/vendas/backup/relatorio.txt >> /home/nycolasdev/ecommerce/vendas/backup/relatorio_fina.txt
    echo "" > relatorio.txt
    #O comando pega todas as linhas existentes em relatorio.txt e envia para dentro de relatorio_fina.txt e depois sobrescre todas as linhas de relatorio 
```
Como esse script foi feito para ser usado manualmente não existe necessidade de usar o cron para ele ser executado automaticamente.
Agora só precisamos dar permissões de execução do mesmo.

#### Terminal
```bash
    chmod +x /home/nycolasdev/ecommerce/consolidador_de_processamentos_de_vendas.sh
```