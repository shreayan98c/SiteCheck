from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template('home.html')


@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        input_url = request.form.get('input_url')
        depth = request.form.get('depth')

        api_response = [
            {
                'load_page_time': 0.923541784286499,
                'links': '["https://www.facebook.com/shreayan.chaudhary", "https://twitter.com/ShreayanC", "https://github.com/shreayan98c", "https://www.linkedin.com/in/shreayan98c/", "https://www.instagram.com/sheruuu98c/", "https://linkedin.com/in/shreayan98c/", "https://drive.google.com/file/d/11ebVFbxQaz4FdQligzXXQYXB1S2VfqVD/view?usp=sharing", "https://razorthink.com/invoice-intelligence", "https://razorthink.com/img/platform/heroimage.png", "https://wisopt.com/", "https://www.kaggle.com/shreayan98c", "https://github.com/shreayan98c", "https://github.com/shreayan98c", "https://www.researchgate.net/publication/339131769_Recommendation_System_for_Big_Data_Software_Using_Popularity_Model_and_Collaborative_Filtering", "https://patentscope.wipo.int/search/en/detail.jsf?docId=IN312324266&_cid=P21-KRNWR5-95504-1", "https://www.researchgate.net/profile/Shreayan_Chaudhary", "https://www.researchgate.net/publication/339131769_Recommendation_System_for_Big_Data_Software_Using_Popularity_Model_and_Collaborative_Filtering", "https://patentscope.wipo.int/search/en/detail.jsf?docId=IN312324266&_cid=P21-KRNWR5-95504-1", "https://github.com/shreayan98c/Set-My-Biz", "https://youtu.be/lvfHyByeIXo", "https://censusindia.gov.in/2011census/population_enumeration.html", "https://github.com/VenterProject/Venter_CMS", "https://grad-search.herokuapp.com/", "https://github.com/shreayan98c/Smart-Assistant", "https://github.com/shreayan98c/Movie-Recommender-System", "https://grouplens.org/datasets/movielens/", "https://github.com/ctrl-alt-code-iot-hackathon/HornOKPlease", "https://local-lib-app.herokuapp.com/", "https://github.com/shreayan98c/Library-App", "https://github.com/shreayan98c/ZS-Hiring-Challenge", "https://news-blog-app.herokuapp.com/", "https://github.com/shreayan98c/News-Blog", "https://github.com/shreayan98c/Fashion-MNIST", "https://github.com/shreayan98c/Face-Detection", "https://github.com/shreayan98c/Maven-Web-Application", "https://github.com/shreayan98c/House-Pricing-Prediction", "https://archive.ics.uci.edu/ml/machine-learning-databases/housing/housing.names", "https://github.com/shreayan98c/Breast-Cancer-EDA", "https://archive.ics.uci.edu/ml/datasets/Breast+Cancer+Wisconsin+%28Diagnostic%29", "https://github.com/shreayan98c/IBM-HR-Analytics", "https://www.kaggle.com/pavansubhasht/ibm-hr-analytics-attrition-dataset", "https://github.com/shreayan98c/IITB-Web-Assignment", "https://www.facebook.com/shreayan.chaudhary", "https://twitter.com/ShreayanC", "https://github.com/shreayan98c", "https://www.linkedin.com/in/shreayan98c/", "https://www.instagram.com/sheruuu98c/"]',
                'images': '["<img alt=\\"Cannot load image.\\" class=\\"profile-pic\\" src=\\"images/profilepic.JPG\\"/>"]',
                'check_imgs_time': '0.5505821704864502',
                'tag_counts': '{"br": 67, "span": 63, "a": 61, "p": 55, "div": 51, "li": 35, "b": 35, "h3": 29, "hr": 20, "em": 16, "i": 13, "script": 9, "blockquote": 8, "cite": 8, "h1": 7, "ul": 6, "mark": 6, "strong": 6, "link": 5, "section": 5, "meta": 4, "h2": 4}',
                'lang_counts': '{"en": 1}',
                'local_links': '["https://www.cs.jhu.edu/~schaud31/", "https://www.cs.jhu.edu/~schaud31/projects/todoList/index.html"]',
                'nonlocal_links': '["https://www.facebook.com/shreayan.chaudhary", "https://twitter.com/ShreayanC", "https://github.com/shreayan98c", "https://www.linkedin.com/in/shreayan98c/", "https://www.instagram.com/sheruuu98c/", "mailto:shreayan98c@gmail.com", "https://linkedin.com/in/shreayan98c/", "https://drive.google.com/file/d/11ebVFbxQaz4FdQligzXXQYXB1S2VfqVD/view?usp=sharing", "https://razorthink.com/invoice-intelligence", "https://razorthink.com/img/platform/heroimage.png", "https://wisopt.com/", "https://www.kaggle.com/shreayan98c", "https://github.com/shreayan98c", "https://github.com/shreayan98c", "https://www.researchgate.net/publication/339131769_Recommendation_System_for_Big_Data_Software_Using_Popularity_Model_and_Collaborative_Filtering", "https://patentscope.wipo.int/search/en/detail.jsf?docId=IN312324266&_cid=P21-KRNWR5-95504-1", "https://www.researchgate.net/profile/Shreayan_Chaudhary", "https://www.researchgate.net/publication/339131769_Recommendation_System_for_Big_Data_Software_Using_Popularity_Model_and_Collaborative_Filtering", "https://patentscope.wipo.int/search/en/detail.jsf?docId=IN312324266&_cid=P21-KRNWR5-95504-1", "https://github.com/shreayan98c/Set-My-Biz", "https://youtu.be/lvfHyByeIXo", "https://censusindia.gov.in/2011census/population_enumeration.html", "https://github.com/VenterProject/Venter_CMS", "https://grad-search.herokuapp.com/", "https://github.com/shreayan98c/Smart-Assistant", "https://github.com/shreayan98c/Movie-Recommender-System", "https://grouplens.org/datasets/movielens/", "https://github.com/ctrl-alt-code-iot-hackathon/HornOKPlease", "https://local-lib-app.herokuapp.com/", "https://github.com/shreayan98c/Library-App", "https://github.com/shreayan98c/ZS-Hiring-Challenge", "https://news-blog-app.herokuapp.com/", "https://github.com/shreayan98c/News-Blog", "https://github.com/shreayan98c/Fashion-MNIST", "https://github.com/shreayan98c/Face-Detection", "https://github.com/shreayan98c/Maven-Web-Application", "https://github.com/shreayan98c/House-Pricing-Prediction", "https://archive.ics.uci.edu/ml/machine-learning-databases/housing/housing.names", "https://github.com/shreayan98c/Breast-Cancer-EDA", "https://archive.ics.uci.edu/ml/datasets/Breast+Cancer+Wisconsin+%28Diagnostic%29", "https://github.com/shreayan98c/IBM-HR-Analytics", "https://www.kaggle.com/pavansubhasht/ibm-hr-analytics-attrition-dataset", "https://github.com/shreayan98c/IITB-Web-Assignment", "https://www.facebook.com/shreayan.chaudhary", "https://twitter.com/ShreayanC", "https://github.com/shreayan98c", "https://www.linkedin.com/in/shreayan98c/", "https://www.instagram.com/sheruuu98c/"]',
                'accessibility_violations': '[["color-contrast", "Ensures the contrast between foreground and background colors meets WCAG 2 AA contrast ratio thresholds", "Elements must have sufficient color contrast", "serious"], ["empty-heading", "Ensures headings have discernible text", "Headings must not be empty", "minor"], ["heading-order", "Ensures the order of headings is semantically correct", "Heading levels should only increase by one", "moderate"], ["landmark-one-main", "Ensures the page has only one main landmark and each iframe in the page has at most one main landmark", "Page must have one main landmark", "moderate"], ["link-name", "Ensures links have discernible text", "Links must have discernible text", "serious"], ["meta-viewport", "Ensures <meta name=\\"viewport\\"> does not disable text scaling and zooming", "Zooming and scaling must not be disabled", "critical"], ["region", "Ensures all page content is contained by landmarks", "All page content must be contained by landmarks", "moderate"]]',
                'hierarchy': '{"": {"www.cs.jhu.edu": {"~schaud31": {"": {}, "projects": {"todoList": {"index.html": {}}}}}}}'
            },
            {
                'load_page_time': 0.09294581413269043,
                'links': '[]',
                'images': '[]',
                'check_imgs_time': '0.0',
                'tag_counts': '{"link": 3, "meta": 2, "ul": 2}',
                'lang_counts': '{}',
                'local_links': '[]',
                'nonlocal_links': '[]',
                'accessibility_violations': '[["button-name", "Ensures buttons have discernible text", "Buttons must have discernible text", "critical"], ["color-contrast", "Ensures the contrast between foreground and background colors meets WCAG 2 AA contrast ratio thresholds", "Elements must have sufficient color contrast", "serious"], ["html-has-lang", "Ensures every HTML document has a lang attribute", "<html> element must have a lang attribute", "serious"], ["label", "Ensures every form element has a label", "Form elements must have labels", "critical"], ["landmark-one-main", "Ensures the page has only one main landmark and each iframe in the page has at most one main landmark", "Page must have one main landmark", "moderate"], ["meta-viewport", "Ensures <meta name=\\"viewport\\"> does not disable text scaling and zooming", "Zooming and scaling must not be disabled", "critical"], ["page-has-heading-one", "Ensure that the page, or at least one of its frames contains a level-one heading", "Page must contain a level-one heading", "moderate"]]',
                'hierarchy': '{}'
            }
        ]

        return render_template('dashboard.html', input_url=input_url, depth=depth, url='/static/images/jhu_logo_1.png',
                               responses=api_response)


if __name__ == '__main__':
    app.run(debug=True)
