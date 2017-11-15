cd team
./node_modules/.bin/webpack

cd ..

source ./team/venv/bin/activate
flask --app=team serve -p 5050
