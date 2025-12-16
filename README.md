# site_my_ml
```bash
docker build -t site_ml . 
```

```bash
 docker run --rm -p 5000:5000 --env-file .env site_ml
```