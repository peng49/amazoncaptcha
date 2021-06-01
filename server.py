# -*- coding: utf-8 -*-
import web
import json, uuid, base64, re, os
from amazoncaptcha import AmazonCaptcha

# from PIL import Image, ImageFile

# ImageFile.LOAD_TRUNCATED_IMAGES = True

urls = (
    '/', 'Index'
)


class Index:
    def GET(self):
        captcha = AmazonCaptcha.fromlink(web.input('url').url)
        solution = captcha.solve()
        return json.dumps({'code': 200, 'message': 'Success', 'data': solution})

    def POST(self):
        input = web.input('image') # 验证码图片base64编码

        image = re.sub(r' ', '+', input.image)

        # 通过base64生成缓存图片
        filename = '/tmp/'+str(uuid.uuid4())+'.jpg'
        file = open(filename,'wb+')
        file.write(base64.standard_b64decode(image))
        file.close()
        print(filename)
        # 解析缓存图片获取验证码
        solution = AmazonCaptcha(filename).solve()

        print(solution)

        #todo 删除缓存图片
        os.remove(filename)

        return json.dumps({'code': 200, 'message': 'Success', 'data': solution})

if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()