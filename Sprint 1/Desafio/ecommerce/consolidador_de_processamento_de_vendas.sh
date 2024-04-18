#!/bin/bash
cd /home/nycolasdev/ecommerce/vendas/backup/
head -n 999999999 /home/nycolasdev/ecommerce/vendas/backup/relatorio.txt >> /home/nycolasdev/ecommerce/vendas/backup/relatorio_fina.txt
echo "" > relatorio.txt
