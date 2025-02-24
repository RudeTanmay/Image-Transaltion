import os
import cv2
import numpy as np
from flask import Flask, render_template, request, redirect, url_for, jsonify
from tensorflow.keras.layers import Layer
from tensorflow.keras.models import load_model
import matplotlib.pyplot as plt
import tensorflow as tf

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

class Sampling(tf.keras.layers.Layer):
    def call(self, inputs):
        z_mean, z_log_var = inputs
        batch = tf.shape(z_mean)[0]
        dim = tf.shape(z_mean)[1]
        epsilon = tf.keras.backend.random_normal(shape=(batch, dim))
        return z_mean + tf.exp(0.5 * z_log_var) * epsilon

# Load models with explicit TensorFlow context
with tf.init_scope():
    ct_to_mri_model = load_model('models/ct_to_mri_epoch_39.h5', 
                               custom_objects={'Sampling': Sampling})
    mri_to_ct_model = load_model('models/mri_to_ct_epoch_39.h5',
                               custom_objects={'Sampling': Sampling})

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def process_image(image_path, model):
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Could not load image")
    
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (256, 256))
    img = img.astype(np.float32) / 255.0
    img = np.expand_dims(img, axis=0)
    
    prediction = model.predict(img)
    if isinstance(prediction, (list, tuple)):
        prediction = prediction[0]
    
    prediction = np.squeeze(prediction)
    prediction = (prediction * 255).astype(np.uint8)
    return prediction

def clean_uploads():
    upload_dir = app.config['UPLOAD_FOLDER']
    for filename in os.listdir(upload_dir):
        file_path = os.path.join(upload_dir, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f'Error deleting {file_path}: {e}')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/try_now')
def try_now():
    return render_template('try_now.html')

@app.route('/samples')
def samples():
    return render_template('samples.html')

@app.route('/model_info')
def model_info():
    return render_template('model_info.html')

@app.route('/translate', methods=['POST'])
def translate():
    clean_uploads()  # Clean previous uploads
    
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        # Save original image
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], 'original.png')
        file.save(upload_path)
        
        # Choose model based on translation direction
        direction = request.form.get('direction')
        model = ct_to_mri_model if direction == 'ct_to_mri' else mri_to_ct_model
        
        try:
            result = process_image(upload_path, model)
            result_path = os.path.join(app.config['UPLOAD_FOLDER'], 'result.png')
            plt.imsave(result_path, result)
            
            return render_template('result.html', 
                                original=url_for('static', filename='uploads/original.png'),
                                result=url_for('static', filename='uploads/result.png'))
        except Exception as e:
            return f"Error processing image: {str(e)}"
    
    return redirect(url_for('try_now'))

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(host='0.0.0.0', port=5000, debug=False)  # Set debug=False for production