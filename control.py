from flask import Flask,request
import json, requests
import subprocess,re, traceback
 
app=Flask(__name__)
 

# def recv_command_respon():
#     """运行完后，将结果返回"""


# 只接受get方法访问
@app.route("/command",methods=["POST"])
def check():
    # 默认返回内容
    return_dict= {'return_code': '200', 'return_info': '处理成功', 'result': False}
    # 判断入参是否为空
    if request.args is None:
        return_dict['return_code'] = '5004'
        return_dict['return_info'] = '请求参数为空'
        return json.dumps(return_dict, ensure_ascii=False)
    # 获取传入的params参数
    # get_data=request.args.to_dict()
    get_data=request.json
    print(get_data)
    command_list = json.loads(get_data.get('command'))
    try:
        export_dict = json.loads(get_data.get('export_dict'))
        for key in export_dict:
            with open('opera.sh', 'a') as f:
                f.write(f'export {key}={export_dict[key]}\n') 
    except:
        pass
    # 对参数进行操作
    work_path = ''
    for command in command_list:
        one_command = ' '.join(command)   
        print(one_command)
        # 将命令写入 a.sh 文件中
        with open('opera.sh', 'a') as f:
            f.write(f'{one_command}\n')   
    out = subprocess.run(['bash', 'opera.sh'], capture_output=True, text=True).stdout
    return_dict['result'] = True
    return_dict['out'] = out
    subprocess.run(['rm', '-f', 'opera.sh'])
    base_info = json.loads(get_data.get('base_info'))
    if base_info['opera'] in ['启动服务', '重启服务']:
        remote_addr = base_info['remote_addr']
        url = f"http://{remote_addr}/admin/server_bot/recv_command_respon/"
        body = {
            'base_info':json.dumps(base_info),
        }
        requests.get(url, params=body)  # 发送请求
    return json.dumps(return_dict, ensure_ascii=False)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
