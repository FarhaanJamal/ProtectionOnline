from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
import time
import threading
import r1_1_ssl
import r1_2_safe_browsing
import r1_3_crowdsource
import r1_5_rnn





app = Flask(__name__)
CORS(app)

stored_url = None  
stored_progress =10
sslc_status = 0
google_safe_browsing_status = 0
stored_review = None
privacy_text = '''1. This website collects personal information such as name, contact number, email address, communication address, date of birth, gender, zip code, lifestyle information, demographic and work details provided by you to us or third-party business partners that operate platforms where you can earn loyalty points for purchase of goods and services, and/or redeem them.
2. This website cogr4bgfbgfबिलिंग पता, क्रेडिट/डेबिट कार्ड नंबर, क्रेडिट/डेबिट कार्ड की समाप्ति तिथि, और/या अन्य भुगतान साधन विवरण और सेवाएं प्रदान करने, लेनदेन सक्षम करने या रिफंड के लिए चेक या मनी ऑर्डर से ट्रैकिंग जानकारी मांग सकती है। रद्द किए गए लेनदेन के लिए.
4. यह वेबसाइट वह यूआरएल एकत्र करती है जहां से आप अभी आए हैं (चाहे यह यूआरएल हमारे प्लेटफॉर्म पर है या नहीं), आप अगली बार किस यूआरएल पर जाएंगे (चाहे यह यूआरएल हमारे प्लेटफॉर्म पर है या नहीं), आपके कंप्यूटर ब्राउज़र की जानकारी और आपका आईपी पता .
5. यह वेबसाइट सेवाएं प्रदान करने, लेनदेन को सक्षम करने, या रद्द किए गए लेनदेन के लिए धनवापसी के उद्देश्य से डेटा एकत्र करती है।
'''
stored_reg_text = '''No violation ofआईटी अधिनियम 2009 के संबंध में गोपनीयता नीति का कोई उल्लंघन नहीं।''' 
stored_crowd_source_info = "Safe:15 | Unsafe:0" 
lock = threading.Lock()

# @app.route('/')
# def all_data_disp(stored_url):
#     global sslc_status, google_safe_browsing_status, rnn,stored_crowd_source_info, get_prog, csi
#     sslc_status = r1_1_ssl.ValidateSsl(stored_url)
#     google_safe_browsing_status = r1_2_safe_browsing.CheckUrl(stored_url)
#     csi = r1_3_crowdsource.SearchUrl(stored_url)
#     rnn = r1_5_rnn.rnn_model(stored_url)
#     get_prog = 100








@app.route('/receive_url', methods=['POST'])
def receive_url():
    global stored_url
    url = request.json.get('url')
    print(f'Received URL: {url}')
    stored_url = url
    # all_data_disp(stored_url)
    return jsonify({'status': 'success'})

@app.route('/get_progress')
def get_progress():
        return jsonify({'progress': stored_progress})

@app.route('/get_sslc')
def get_sslc():
        return jsonify({'SSLC': sslc_status[0]+" "+sslc_status[2]})

@app.route('/get_safe_browsing_status')
def get_safe_browsing_status():
        return jsonify({'Google_Safe_Browsing_Status': str(google_safe_browsing_status)+""+str(rnn)})


@app.route('/get_crowd_source_info')
def get_crowd_source_info():
        return jsonify({'crowd_source_info': csi})



@app.route('/expiry')
def expiry():
        Expiry = sslc_status[1]
        return jsonify({'Expiry': Expiry})

@app.route('/submit_review', methods=['POST'])
def submit_review():
    global stored_review
    review = request.json.get('review')
# Store the review as 0 for 'bad' and 1 for 'good'        
    stored_review = 1 if review == 'Safe' else 0
    print(f'Received Review: {review} (Stored as: {stored_review})')
    return jsonify({'status': 'success'})

@app.route('/get_review')
def get_review():
    global stored_review
    return jsonify({'review': stored_review})




@app.route('/get_privacy')
def get_privacy():
    global out

    global privacy_text
    time.sleep(5)
    out = ["8"]*4
    return jsonify({'Privacy': out[0]+"\n"+out[1]})



@app.route('/get_reg_text')
def get_reg_text():
    global stored_reg_text
    return jsonify({'reg_text': out[2]+"\n"+out[3]})


if __name__ == '__main__':
    app.run(debug=True)

