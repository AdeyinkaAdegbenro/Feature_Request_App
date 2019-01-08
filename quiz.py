from cryptography.fernet import Fernet

key = 'TluxwB3fV_GWuLkR1_BzGs1Zk90TYAuhNMZP_0q4WyM='

# Oh no! The code is going over the edge! What are you going to do?
message = b'gAAAAABcMiwbvnL4t3YFgMG8KCB_b78MKGyZHfQ_7GsZHNtHbpIzpMmgrO0-9hJTDJ5B2D54HlkKMMtT9PwB5HmSqpFJ10SPR-5xD0y0WAJ6Pfpc5APRkp77Zt4VJR9hHNViJ6pnJtE4vJ4BKWJ90I49tiosqvgYgsUh-dhc7JYtKAwb0CT830CSEeVW46FWRJ-MQgu1c4lO'

def main():
    f = Fernet(key)
    print(f.decrypt(message))


if __name__ == "__main__":
    main()