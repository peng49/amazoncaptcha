# -*- coding: utf-8 -*-
import web
import json, uuid, base64, re, os
from amazoncaptcha import AmazonCaptcha

urls = (
    '/', 'Index'
)


class Index:
    def GET(self):
        try:
            captcha = AmazonCaptcha.fromlink(web.input('url').url)
            solution = captcha.solve()
            return json.dumps({'code': 200, 'message': 'Success', 'data': solution})
        except (KeyError, AttributeError):
            return json.dumps({'code': 400, 'error': '参数错误'})
        except:
            return json.dumps({'code': 500, 'error': '服务异常'})

    def POST(self):
        try:
            if re.search(r'application/json', str(web.ctx.env.get('CONTENT_TYPE')), re.I) is not None:
                # application/json
                input = json.loads(web.data())
            else:
                input = web.input('image')  # 验证码图片base64编码

            image = re.sub(r' ', '+', input['image'])

            # 通过base64生成缓存图片
            filename = '/tmp/' + str(uuid.uuid4()) + '.jpg'
            file = open(filename, 'wb+')
            file.write(base64.standard_b64decode(image))
            file.close()

            # 解析缓存图片获取验证码
            solution = AmazonCaptcha(filename).solve()

            # 删除缓存图片
            os.remove(filename)

            return json.dumps({'code': 200, 'message': 'Success', 'data': solution})
        except (KeyError, AttributeError) as e:
            return json.dumps({'code': 400, 'error': '参数错误:'+str(e)})
        except BaseException as e:
            return json.dumps({'code': 500, 'error': '服务异常:'+str(e)})


if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()
