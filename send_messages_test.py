from twilio.rest import Client
import serial
from time import sleep


def split_values(values):
    heart_rate, spo2 = values.split('/')
    spo2 = spo2.split('\r')
    return heart_rate, spo2[0]

def get_max_values(heart_rate_values, spo2_values):
    max_heart_rate_value = max(heart_rate_values)
    max_spo2_value = max(spo2_values)
    return max_heart_rate_value, max_spo2_value

def valid_spo2_value(max_spo2_value):
    if max_spo2_value < 100 and max_spo2_value > 40:
        return True
    return False

def valid_heart_rate_value(max_heart_rate_value):
    if max_heart_rate_value < 50 or max_heart_rate_value > 150:
        return True
    return False

def send_message(message):
    client.messages.create(
        body = message,
        from_ = 'whatsapp:+14155238886',
        to = 'whatsapp:+5512988994326'
    )


serial_setting = serial.Serial('COM6', 115200)

account_sid = "AC45bf0f64189355258217e17b6d0dd109"
auth_token = "6f63df0e848b10b959fd1ea0c6177e25"
client = Client(account_sid, auth_token) 

count = 0
heart_rate_values = list()
spo2_values = list()
incorrect_values = ["ets Jun  8 2016 00:22:57\r\n", "\r\n", "rst:0x1 (POWERON_RESET),boot:0x13 (SPI_FAST_FLASH_BOOT)\r\n", "configsip: 0, SPIWP:0xee\r\n", "clk_drv:0x00,q_drv:0x00,d_drv:0x00,cs0_drv:0x00,hd_drv:0x00,wp_drv:0x00\r\n", "clk_drv:0x00,q_drv:0x00,d_drv:0x00,cs0_drv:0x00,hd_drv:0x00,wp_drv:0x00\r\n", "mode:DIO, clock div:1\r\n", "load:0x3fff0018,len:4\r\n", "load:0x3fff001c,len:1216\r\n", "ho 0 tail 12 room 4\r\n", "load:0x40078000,len:10944\r\n", "load:0x40080400,len:6388\r\n", "entry 0x400806b4\r\n", "Beat!\r\n"]

while True:
    while serial_setting.inWaiting():
        values = serial_setting.readline().decode()
        if values not in incorrect_values:
            print(values)
            heart_rate, spo2 = split_values(values)
            heart_rate_values.append(float(heart_rate))
            spo2_values.append(int(spo2))

            count += 1

            if count == 25:
                max_heart_rate_value, max_spo2_value = get_max_values(heart_rate_values, spo2_values)
                count = 0
                heart_rate_values = list()
                spo2_values = list()

                if valid_heart_rate_value(max_heart_rate_value):
                    message = "Alerta!!! Seu nível de batimentos cardíacos estão fora do normal, procure um médico."
                    send_message(message)
                if valid_spo2_value(max_spo2_value):
                    message = f"Alerta!!! Seu nível de oxigenação sanguínea está em {max_spo2_value}%. Procure um médico imediatamente!"
                    send_message(message)

                sleep(30)
