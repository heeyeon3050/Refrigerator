import socket
from Service import Service
from ocr_date import receiveImg
import cv2
import numpy as np


def get_bytes_stream(sock, s_length):
    buffer = b''
    try:
        remain = s_length
        while True:
            data = sock.recv(remain)
            buffer += data
            if len(buffer) == s_length:
                break
            elif len(buffer) < s_length:
                remain = s_length - len(buffer)
    except Exception as e:
        print(e)
    return buffer[:s_length]


def main():
    host = '112.185.33.172'  # 호스트 ip를 적어주세요
    port = 57000  # 포트번호를 임의로 설정해주세요

    service = Service()
    server_sock = socket.socket(socket.AF_INET)
    server_sock.bind((host, port))
    server_sock.listen(1)
    print("연결 대기 중..")

    while True:
        client_sock, addr = server_sock.accept()  # 연결 승인
        print('연결 주소 : ', addr)

        try:
            len_bytes_string = bytearray(client_sock.recv(1024))[2:]
            len_bytes = len_bytes_string.decode('utf-8')
        except:
            print("데이터 수신 실패")
            pass

        if len_bytes[0:7] == 'Product':     # 바코드 검색
            result = str(service.Search_P(len_bytes[7:]))
            print(result)

            if result == "None":
                result = ''

            result = result.encode("UTF-8")
            client_sock.send(len(result).to_bytes(2, byteorder='big'))
            client_sock.send(result)
            print("데이터 송신 완료")

        elif len_bytes[0:6] == 'Recipe':    # 레시피 검색
            food_arr = list(map(str, len_bytes[6:].split()))
            print(food_arr)
            result = service.Search_R()

            recipe_arr = [[0 for j in range(2)] for i in range(len(result))]
            cnt = [0] * len(result)
            start = 0

            # 받아온 데이터값을 2차원 배열로 수정
            for i in result:
                recipe_arr[start][0] = i.F_Name
                recipe_arr[start][1] = i.Thing1 + i.Thing2 + i.Thing3
                start = start + 1

            for i in food_arr:
                for j in range(len(result)):
                    if i in recipe_arr[j][1]:
                        cnt[j] += 1

            f_name = ''

            for i in range(len(cnt)):
                if cnt[i] > 2:
                    f_name += recipe_arr[i][0] + "#"

            if len(f_name) == 0:
                send_result = ''
            else:
                send_result = f_name[:-1:]

            print(send_result)

            send_result = send_result.encode("UTF-8")
            client_sock.send(len(send_result).to_bytes(2, byteorder='big'))
            client_sock.send(send_result)
            print("데이터 송신 완료")

        elif len_bytes[0:5] == 'check':     # 로그인 할때 냉장고 이름 들고오는 메서드
            id, pw = map(str, len_bytes[5:].split('#'))
            datas = [id, pw]
            result = str(service.Login_Check(datas))

            if result == "None":
                result = ''

            result = result.encode("UTF-8")
            client_sock.send(len(result).to_bytes(2, byteorder='big'))
            client_sock.send(result)
            print("데이터 송신 완료")

        elif len_bytes[0:6] == 'Insert':     # 회원가입 메서드
            id, pw, name, email = map(str, len_bytes[6:].split('#'))
            insert_datas = [id, pw, name, email]
            result = service.Insert_U(insert_datas)     # 결과값 "성공" 아니면 "중복"임

            result = result.encode("UTF-8")
            client_sock.send(len(result).to_bytes(2, byteorder='big'))
            client_sock.send(result)
            print("데이터 송신 완료")

        else:   # 유통기한 인식
            length = int(len_bytes)

            img_bytes = get_bytes_stream(client_sock, length)
            img_path = "./date01.jpg"

            with open(img_path, 'wb') as writer:
                writer.write(img_bytes)
            print(img_path + " is saved")

            d_img = cv2.imread('date01.jpg', cv2.IMREAD_COLOR)
            # 이미지 이진화
            gray = cv2.cvtColor(d_img, cv2.COLOR_BGR2GRAY)
            ret, dst = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)
            # cv2.imshow("dst", dst)

            # 구조화 요소 커널, 사각형 (3x3) 생성 ---①
            k = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
            # 침식 연산 적용 ---②
            erosion = cv2.erode(dst, k)

            # 결과 출력
            merged = np.hstack((dst, erosion))
            # cv2.imshow('Erode', merged)

            # cv2.waitKey(0)
            # cv2.destroyAllWindows()

            chars = receiveImg(d_img, '418dd09991a16ad0c410f4a38dcf5927')  # 카카오 OCR API
            chars = chars.replace(" ", "")
            result_chars = ''
            try:
                if chars.count('.') == 2 or chars.count(',') == 2 or chars.count('.') + chars.count(',') == 2\
                        :
                    year, month, day = map(str, chars.split("."))
                    result_chars = year[-2:] + month + day[0:2]
            except IOError or IndexError:
                print("유통 기한 인식 실패")
                result_chars = ''


            """
            for c in chars:
                if c.isdigit():
                    result_chars += c
            result_chars = result_chars[-6:]
            """
            print(result_chars)

            result_chars = result_chars.encode("UTF-8")
            client_sock.send(len(result_chars).to_bytes(2, byteorder='big'))
            client_sock.send(result_chars)
            print(result_chars)
            print("데이터 송신 완료")


if __name__ == "__main__":
    print("MySQL DB 연결 시도")
    main()
