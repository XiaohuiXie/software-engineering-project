from DarkBoard import app

from waitress import serve

'''
Starts service
'''
if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=80)