from flask import Flask, render_template, request
import joblib

# Load the model and scaler
model = joblib.load('startup_rf_model.pkl')

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Retrieve input values from the form
    age_first_funding = float(request.form['age_first_funding'])
    age_last_funding = float(request.form['age_last_funding'])
    age_first_milestone = float(request.form['age_first_milestone'])
    age_last_milestone = float(request.form['age_last_milestone'])
    relationships = float(request.form['relationships'])
    funding_rounds = float(request.form['funding_rounds'])
    total_funding = float(request.form['total_funding'])
    milestones = float(request.form['milestones'])
    avg_participants = float(request.form['avg_participants'])

    # Create a list with the input data
    input_data = [[
        age_first_funding,
        age_last_funding,
        age_first_milestone,
        age_last_milestone,
        relationships,
        funding_rounds,
        total_funding,
        milestones,
        avg_participants
    ]]

    # Make a prediction
    probabilities = model.predict_proba(input_data)
    
    # Get the probability of success (assuming class 1 is 'Acquired'/'Success')
    success_prob = probabilities[0][1]
    
    # Determine outcome based on the 0.65 threshold
    outcome = "success" if success_prob >= 0.70 else "failure"
    
    # Format the result string
    result = f"the startup has {success_prob:.2%} of success, likely to be {outcome}"

    return render_template('result.html', result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
