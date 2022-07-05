from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
import sqlite3


class RequestHandler(BaseHTTPRequestHandler):

    def send_response_to_client(self, status_code, data):
        self.send_response(status_code)
        self.send_header('Content/type', 'text/plain')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(str(data).encode())

    def do_GET(self):
        self.log_message('Incoming GET request...')

        try:
            index_num = parse_qs(self.path[2:])['index_num'][0]
        except:
            self.send_response_to_client(404, 'Incorrect parameters provided.')
            self.log_message('Incorrect parameters provided.')
            return

        conn = sqlite3.connect('Student.db')
        cursor = conn.cursor()

        cursor.execute(
            '''
            SELECT * FROM students
            WHERE index_num = "{}";'''.format(index_num)
        )

        result = cursor.fetchall()
        cursor.close()
        conn.close()

        if len(result) != 0:
            self.send_response_to_client(200, result[0])
        else:
            self.send_response_to_client(404, 'Index number not found.')
            self.log_message('Index number not found.')

    def do_POST(self):
        self.log_message('Incoming POST request...')
        data = parse_qs(self.path[2:])

        name = data['name'][0]
        surname = data['surname'][0]
        index_num = data['index_num'][0]
        gpa = data['gpa'][0]
        response_post = {
            'name': name,
            'surname': surname,
            'index_num': index_num,
            'gpa': gpa
        }
        self.send_response_to_client(200, response_post)

        conn = sqlite3.connect('Student.db')
        cursor = conn.cursor()

        try:
            cursor.execute(
                '''
                INSERT INTO students (name, surname, index_num, gpa)
                VALUES ("{}", "{}", "{}", {});'''.format(name, surname, index_num, gpa)
            )

            cursor.close()
            conn.commit()
            conn.close()
            self.send_response_to_client(200, response_post)
        except:
            self.send_response_to_client(404, 'Incorrect parameters provided.')
            self.log_message('Incorrect parameters provided by client.')


server_address = ('127.0.0.1', 8080)
print(
    'Starting HTTP server @ {}:{}.'.format(server_address[0], server_address[1]))
http_server = HTTPServer(server_address, RequestHandler)
http_server.serve_forever()
