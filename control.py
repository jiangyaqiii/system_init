from flask import Flask,request
import json, requests
import subprocess,re, traceback
from apscheduler.schedulers.background import BackgroundScheduler

##定时模块
scheduler = BackgroundScheduler()
scheduler.start()

app=Flask(__name__)
 

# def recv_command_respon():
#     """运行完后，将结果返回"""

def _opera_command(command_list):
    """对指令列表进行操作"""
    for command in command_list:
        one_command = ' '.join(command)   
        # 将命令写入 a.sh 文件中
        with open('opera.sh', 'a') as f:
            f.write(f'{one_command}\n')   
    out = subprocess.run(['bash', 'opera.sh'], capture_output=True, text=True).stdout
    return out

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
    get_data = request.json if not request.args.to_dict() else request.args.to_dict()
    command_list = json.loads(get_data.get('command'))
    try:
        export_dict = json.loads(get_data.get('export_dict'))
        for key in export_dict:
            with open('opera.sh', 'a') as f:
                f.write(f'export {key}={export_dict[key]}\n') 
    except:
        pass
    # 对参数列表进行操作，返回具体的执行输出
    out = _opera_command(command_list)
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

@app.route("/start_send_log",methods=['POST'])
def start_send_log():
    """接收到此请求，开始发送日志到服务器tcp服务"""
    source_addr = request.remote_addr
    get_data = request.json if not request.args.to_dict() else request.args.to_dict()
    command_list = json.loads(get_data.get('command'))
    log_obj.start_send_log(command_list, source_addr, 81) ##启动发送日志功能
    return json.dumps({'return_code': '200'}, ensure_ascii=False)

@app.route("/check_alive",methods=['GET'])
def check_alive():
    """检查控制面板活性"""
    return json.dumps({'return_code': '200'}, ensure_ascii=False)


import socket
class Log:
    def __init__(self):
        self.status = False ##默认关闭发送日志按钮
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.command_list = [] ##此项目执行查看日志所需要执行的命令列表
    
    def start_send_log(self, command_list, SERVER_HOST, SERVER_PORT):
        self.status = True
        self.command_list = command_list
        self._socket.connect((SERVER_HOST, SERVER_PORT))

    def send_log(self):
        # 在这里定义您的定时任务逻辑
        # 发送数据到服务器
        if self.status:
            print('开始发送日志')
            out = _opera_command(self.command_list)
            print(self.command_list)
            self._socket.sendall((out+'///delimiter').encode())


log_obj = Log()
# 每隔5秒执行一次my_job()

# def test():
#     out = 'asdadasdad'
#     _socket.sendall((out+'///delimiter').encode())

# _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# _socket.connect(('45.130.21.54', 81))
scheduler.add_job(log_obj.send_log, 'interval', seconds=1)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
