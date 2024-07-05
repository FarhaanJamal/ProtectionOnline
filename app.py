from flask import Flask, request, jsonify
from flask_cors import CORS
import r1_1_ssl
import r1_2_safe_browsing
import r1_3_crowdsource
import r1_5_rnn
import far6_test
import far1_main
from urllib.parse import urlparse


app = Flask(__name__)
CORS(app)


@app.route("/process-url", methods=["POST"])
def process_url():
    points = 0

    url_data = str(request.json["url"])
    domain = urlparse(url_data).netloc

    ssl = r1_1_ssl.ValidateSsl(url_data).split(",")
    safe = r1_2_safe_browsing.CheckUrl(str(url_data))
    rnn_model = r1_5_rnn.rnn_model(url_data)
    csi = r1_3_crowdsource.SearchUrl(domain)
    llm_out = far1_main.mainCombined(url_data)
    print(domain)

    sslc = ssl[0]
    if sslc == "Secure Connection":
        points += 2
    else:
        points += 0


    cookie = ssl[1]
    print(ssl)

    if safe == "SAFE URL":
        points+= 3
    else:
        points += 0
    

    if rnn_model == "Good":
        points += 3
    else:
        points += 0

    
    vote = f"SAFE : {csi[0]} | UNSAFE : {csi[1]}"
    if csi[0]>csi[1]:
        points += 2
    else:
        points += 0
        
    privacyeng = llm_out[0]
    privacyhin = llm_out[1]
    laweng = llm_out[2]
    lawhin = llm_out[3]
    points = 10

    all_data = str(
        str(sslc) + str(cookie) + str(safe) +str(rnn_model)+ str(vote) + str(privacyeng) + str(privacyhin) + str(laweng) + str(lawhin)
    )

    processed_data = {
        "SSL": sslc,
        "Cookie_Expiry_Date": cookie,
        "Google_Safe_Browsing": safe,
        "Crowd_Status": vote,
        "PRE": privacyeng,
        "PRH": privacyhin,
        "RCE": laweng,
        "RCH": lawhin,
        "progress": points,
        "all": all_data,
    }
    print(points)

    return jsonify(processed_data)


@app.route("/store-review", methods=["POST"])
def store_review():
    global review_status
    review_data = request.json
    review_value = review_data.get("review")

    # Store the review status
    if review_value == "Safe":
        review_status = 0
    elif review_value == "Unsafe":
        review_status = 1
    print(review_status)
    return jsonify({"message": "Review stored successfully"})


@app.route("/get-review-status", methods=["GET"])
def get_review_status():
    global review_status
    return jsonify({"review_status": review_status})


if __name__ == "__main__":
    app.run(debug=True)
