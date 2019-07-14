from cryptography.fernet import Fernet

key = 'TluxwB3fV_GWuLkR1_BzGs1Zk90TYAuhNMZP_0q4WyM='

# Oh no! The code is going over the edge! What are you going to do?
message = b'gAAAAABc_DXpu90n9BETllXpgKgFFAAirBqpXT_fzrsu8GJIGTKONYfVgcnfGowRT5knQy8JR4RBF2L7nX7GDGI7LeX3mWJ_bKHRJanOfdfnqETnrXPf9sfbdpPAM4WWSnX5aGMTcc6Rc8T3deV3oy8b-0EcFecp5JvT_HVbqxhUFZFRqxoYs14='


def main():
    f = Fernet(key)
    print(f.decrypt(message))


if __name__ == "__main__":
    main()
