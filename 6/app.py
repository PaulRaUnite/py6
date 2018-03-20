def super_ip_checker() -> callable(str):
    def rootkit(s: str) -> bool:
        ip_expected = s.split('.')
        if len(ip_expected) != 4:
            return False
        try:
            for e in ip_expected:
                if not 0 <= int(e) <= 256:
                    return False
            rootkit.hidden_data.append(s)
            return True
        except ValueError:
            pass
    rootkit.hidden_data = list()
    return rootkit


checker = super_ip_checker()
print(checker("is it IP?"))
print(checker("256.10.55.11"))
print(checker.hidden_data)
