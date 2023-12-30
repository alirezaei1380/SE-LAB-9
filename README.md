# Report

In this project we have a simple architecture based on micro-service principles.
We have the services mentioned below:
- Backend service using python/Django framework
- Database service using PostgreSQL
- Webserver using Nginx

We have a simple CRUD API in back-end like this:

`{HOST}/back/api/` in which we can create a product using fields in a way mentioned in sample below:

```json
{
    "title": "test",
    "price": 1200
}
```

This API also supports UPDATE/DELETE/READ calls in this way:

`{HOST}/back/api/<product_id>/`


