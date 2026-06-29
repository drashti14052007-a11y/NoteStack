from optimizer import load_models, run_optimizer

load_models()
result = run_optimizer('dairy', [8.0, 3.0, 7.0, 6.0, 7.0])
print('Formulation:', result['formulation'])
print('Predicted:  ', result['predicted_scores'])
print('Confidence: ', result['confidence_pct'], '%')