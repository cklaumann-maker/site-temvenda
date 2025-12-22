#!/bin/bash
echo "📤 Upload Manual do stats.html"
curl -T stats.html "ftp://if0_40283323:bqfvYPo802HiA1@ftpupload.net/htdocs/stats.html" --ftp-pasv --silent --show-error
echo ""
echo "✅ Upload concluído!"
echo ""
echo "⚠️ Se o arquivo ainda não atualizar no servidor, pode ser cache do InfinityFree."
echo "💡 Tente aguardar 5-10 minutos ou contate o suporte do InfinityFree."
