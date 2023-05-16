cat query1.txt 
cat query1.txt | \
curl -s \
-X POST \
-H 'Content-Type: application/json' \
-d @- \
"127.0.0.1:8080/v1/graphql" 
echo " \n"
cat query2.txt
cat query2.txt | \
curl -s \
-X POST \
-H 'Content-Type: application/json' \
-d @- \
"127.0.0.1:8080/v1/graphql" 

