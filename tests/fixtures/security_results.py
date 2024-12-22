"""Fixtures pour les résultats de sécurité."""

SAMPLE_SECURITY_RESULTS = {
    'file': 'test.py',
    'security_issues': [
        {
            'severity': 'HIGH',
            'confidence': 'HIGH',
            'test_name': 'B102',
            'description': 'Use of exec detected',
            'line_number': 3
        }
    ],
    'code_quality': {
        'complexity': 5.0,
        'functions': [
            {
                'name': 'vulnerable_function',
                'complexity': 5,
                'line': 1
            }
        ],
        'unused_code': {
            'variables': [{'name': 'UNUSED_VARIABLE', 'line': 8}],
            'functions': [{'name': 'unused_function', 'line': 6}]
        },
        'style_issues': [
            {
                'type': 'security',
                'message': 'Use of exec() or eval() detected',
                'line': 3
            }
        ]
    },
    'summary': {
        'severity_counts': {'critical': 0, 'high': 1, 'medium': 0, 'low': 0},
        'total_issues': 1,
        'score': 90.0,
        'details': 'Analyse détaillée des problèmes trouvés dans le code'
    }
} 