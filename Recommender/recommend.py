from pymongo import MongoClient
from dataservice import DataService
from cosine_similarity import Helper
import operator
import time
import thread

def calculate_top_5(app, user_download_history):
    similarity = {}
    for u in user_download_history:
        if app in u:
            sim = Helper.cosine_similarity([app], u)
            for apps in u:
                if similarity.has_key(apps):
                    similarity[apps] = similarity[apps] + sim
                else:
                    similarity[apps] = sim

    # The app has not been downloaded, therefore no related history
    if not similarity.has_key(app):
        return

    similarity.pop(app)
    sorted_result = sorted(similarity.items(), key = operator.itemgetter(1), reverse = True)
    top_5 = []
    for i in range(5):
        top_5.append(sorted_result[i][0])
    print str(app) + " - top 5: " + str(top_5)
    DataService.update_app_info({'app_id': app}, {'$set': {'top_5_app': top_5}})

def main():
    try:
        start = time.clock()
        client = MongoClient('localhost', 27017)
        DataService.init(client)

        user_download_history = DataService.retrieve_user_download_history()
        apps = DataService.retrieve_app_info()
        for app in apps.keys():
            calculate_top_5(app, user_download_history.values())
        end = time.clock()
        print "time: " + str(end - start)
    except Exception as e:
        print e
    finally:
        if 'client' in locals():
            client.close()

if __name__ == "__main__":
    main()

