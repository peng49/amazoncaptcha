# amazoncaptcha

安装

> docker run -d -p 8080:8080 --name=amazoncaptcha peng49/amazoncaptcha

使用GET方式调用
```
curl http://localhost:8080?url=https://images-na.ssl-images-amazon.com/captcha/cucusdhr/Captcha_uglxutyncg.jpg
```

使用POST方式调用
```
curl -X POST -d image='验证码图片base64编码' http://localhost:8080
```

返回结果
```json
{"code": 200, "message": "Success", "data": "KMJUJG"}
```




