import requests
import xlsxwriter
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem


software_names = [SoftwareName.CHROME.value]
operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]
user_agent_rotator = UserAgent(
    software_names=software_names, operating_systems=operating_systems, limit=100
)


def itmoparse():
    headers = {"user-agent": user_agent_rotator.get_random_user_agent()}

    dir_info = requests.get(
        "https://abitlk.itmo.ru/api/v1/9e2eee80b266b31c8d65f1dd3992fa26eb8b4c118ca9633550889a8ff2cac429/rating/directions?degree=bachelor",
        headers,
    ).json()
    directions = {}
    abiturients = {}
    print("Parsing started")
    for dir in dir_info["result"]["items"]:
        headers = {"user-agent": user_agent_rotator.get_random_user_agent()}
        dir_list = requests.get(
            f"https://abitlk.itmo.ru/api/v1/rating/bachelor/budget?program_id={dir['isu_id']}&manager_key=&sort=&showLosers=true",
            headers,
        ).json()["result"]
        directions[dir["direction_title"]] = []
        print("Processing", dir["direction_title"])
        for group in [
            "without_entry_tests",
            "by_unusual_quota",
            "by_special_quota",
            "by_target_quota",
            "general_competition",
        ]:
            if dir_list[group]:
                for abit in dir_list[group]:
                    directions[dir["direction_title"]].append(
                        (abit["snils"], abit["case_number"], abit["total_scores"])
                    )
                id = abit[0] if abit[0] else abit[1]
                if id not in abiturients.keys():
                    abiturients[id] = {"score": abit[2], "directions": []}
                abiturients[id]["directions"].append(dir["direction_title"])

    print("Creating file")
    itmo_abiturients = xlsxwriter.Workbook("itmo_abiturients.xlsx")
    worksheet = itmo_abiturients.add_worksheet()
    worksheet.write_row(0, 0, ["СНИЛС/Дело", "Балл", "Направления"])
    for i, abit_id in enumerate(abiturients.keys()):
        worksheet.write(i + 1, 0, abit_id)
        worksheet.write(i + 1, 1, abiturients[abit_id]["score"])
        worksheet.write_row(i + 1, 2, abiturients[abit_id]["directions"])
    itmo_abiturients.close()
    print("File saved as 'itmo_abiturients.xlsx'")


itmoparse()
