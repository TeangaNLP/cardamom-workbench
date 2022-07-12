docker compose down
rm -rf static
cd react_views
npm run build
cd ..
docker compose build
docker compose up