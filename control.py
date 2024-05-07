from flask import Flask,request
import json
import subprocess
 
app=Flask(__name__)
 
# 只接受get方法访问
@app.route("/command",methods=["GET"])
def check():
    # 默认返回内容
    return_dict= {'return_code': '200', 'return_info': '处理成功', 'result': False}
    # 判断入参是否为空
    if request.args is None:
        return_dict['return_code'] = '5004'
        return_dict['return_info'] = '请求参数为空'
        return json.dumps(return_dict, ensure_ascii=False)
    # 获取传入的params参数
    get_data=request.args.to_dict()
    command_list = json.loads(get_data.get('command_list'))
    # 对参数进行操作
    for command in command_list:
        out = subprocess.getoutput(command)
        return_dict[command] = out
    return json.dumps(return_dict, ensure_ascii=False)
 
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
