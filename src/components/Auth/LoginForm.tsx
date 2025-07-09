import React, { useState } from 'react';
import { Mail, Lock, Eye, EyeOff } from 'lucide-react';
import { useAuth } from '../../contexts/AuthContext';

const LoginForm: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [showResetForm, setShowResetForm] = useState(false);
  const [resetEmail, setResetEmail] = useState('');
  const [resetSent, setResetSent] = useState(false);
  const { login, resetPassword, isLoading, error, clearError } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    clearError();
    try {
      await login({ email, password });
    } catch (error) {
      console.error('Login failed:', error);
    }
  };

  const handleReset = async (e: React.FormEvent) => {
    e.preventDefault();
    clearError();
    try {
      await resetPassword(resetEmail);
      setResetSent(true);
    } catch (error) {
      console.error('Reset failed:', error);
    }
  };

  if (showResetForm) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
        <div className="w-full max-w-md">
          <div className="bg-white rounded-xl shadow-lg p-8">
            <div className="text-center mb-8">
              <div className="w-16 h-16 bg-[#72C02C] rounded-full flex items-center justify-center mx-auto mb-4">
                <Mail className="w-8 h-8 text-white" />
              </div>
              <h2 className="text-2xl font-bold text-gray-900">
                Réinitialisation du mot de passe
              </h2>
              <p className="text-gray-600 mt-2">
                Entrez votre email pour recevoir un lien de réinitialisation
              </p>
            </div>

            {error && (
              <div className="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded-lg">
                {error}
              </div>
            )}

            {resetSent ? (
              <div className="text-center">
                <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Mail className="w-8 h-8 text-green-600" />
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">
                  Email envoyé !
                </h3>
                <p className="text-gray-600 mb-6">
                  Vérifiez votre boîte mail pour le lien de réinitialisation
                </p>
                <button
                  onClick={() => setShowResetForm(false)}
                  className="text-[#72C02C] hover:text-[#5da021] font-medium"
                >
                  Retour à la connexion
                </button>
              </div>
            ) : (
              <form onSubmit={handleReset} className="space-y-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Adresse email
                  </label>
                  <div className="relative">
                    <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                    <input
                      type="email"
                      value={resetEmail}
                      onChange={(e) => setResetEmail(e.target.value)}
                      className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#72C02C] focus:border-transparent transition-colors"
                      placeholder="votre@email.com"
                      required
                    />
                  </div>
                </div>

                <button
                  type="submit"
                  disabled={isLoading}
                  className="w-full bg-[#72C02C] text-white py-3 px-4 rounded-lg font-medium hover:bg-[#5da021] focus:ring-2 focus:ring-[#72C02C] focus:ring-offset-2 transition-colors disabled:opacity-50"
                >
                  {isLoading ? 'Envoi en cours...' : 'Envoyer le lien'}
                </button>

                <button
                  type="button"
                  onClick={() => setShowResetForm(false)}
                  className="w-full text-gray-600 hover:text-gray-800 font-medium"
                >
                  Retour à la connexion
                </button>
              </form>
            )}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        <div className="bg-white rounded-xl shadow-lg p-8">
          <div className="text-center mb-8">
            <div className="w-16 h-16 bg-[#72C02C] rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-white font-bold text-xl">CM</span>
            </div>
            <h2 className="text-2xl font-bold text-gray-900">Connexion</h2>
            <p className="text-gray-600 mt-2">
              Connectez-vous à votre espace de gestion
            </p>
          </div>

          {error && (
            <div className="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded-lg">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Adresse email
              </label>
              <div className="relative">
                <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#72C02C] focus:border-transparent transition-colors"
                  placeholder="votre@email.com"
                  required
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Mot de passe
              </label>
              <div className="relative">
                <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                <input
                  type={showPassword ? 'text' : 'password'}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full pl-10 pr-12 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#72C02C] focus:border-transparent transition-colors"
                  placeholder="••••••••"
                  required
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
                >
                  {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                </button>
              </div>
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="w-full bg-[#72C02C] text-white py-3 px-4 rounded-lg font-medium hover:bg-[#5da021] focus:ring-2 focus:ring-[#72C02C] focus:ring-offset-2 transition-colors disabled:opacity-50"
            >
              {isLoading ? 'Connexion...' : 'Se connecter'}
            </button>

            <button
              type="button"
              onClick={() => setShowResetForm(true)}
              className="w-full text-[#72C02C] hover:text-[#5da021] font-medium"
            >
              Mot de passe oublié ?
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default LoginForm;