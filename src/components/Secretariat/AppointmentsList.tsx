import React, { useState } from 'react';
import { Calendar, Clock, User, Plus, Edit, Trash2, Phone, Mail, Check, X } from 'lucide-react';
import { Appointment } from '../../types';

const AppointmentsList: React.FC = () => {
  const [showAddModal, setShowAddModal] = useState(false);
  const [selectedFilter, setSelectedFilter] = useState('all');

  const mockAppointments: Appointment[] = [
    {
      id: '1',
      title: 'Entretien RH',
      client: 'Marie Dubois',
      date: '2024-01-25',
      time: '14:00',
      duration: 60,
      status: 'confirmed',
      notes: 'Entretien annuel de performance'
    },
    {
      id: '2',
      title: 'Consultation IT',
      client: 'Jean Martin',
      date: '2024-01-26',
      time: '10:30',
      duration: 30,
      status: 'scheduled',
      notes: 'Support technique pour le nouvel ERP'
    },
    {
      id: '3',
      title: 'Formation',
      client: 'Sophie Laurent',
      date: '2024-01-24',
      time: '09:00',
      duration: 120,
      status: 'completed',
      notes: 'Formation sur les nouveaux processus'
    },
    {
      id: '4',
      title: 'Réunion projet',
      client: 'Pierre Moreau',
      date: '2024-01-27',
      time: '16:00',
      duration: 45,
      status: 'cancelled',
      notes: 'Annulé par le client'
    }
  ];

  const filteredAppointments = mockAppointments.filter(appointment => {
    if (selectedFilter === 'all') return true;
    return appointment.status === selectedFilter;
  });

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'scheduled': return 'bg-blue-100 text-blue-800';
      case 'confirmed': return 'bg-green-100 text-green-800';
      case 'completed': return 'bg-gray-100 text-gray-800';
      case 'cancelled': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusLabel = (status: string) => {
    switch (status) {
      case 'scheduled': return 'Programmé';
      case 'confirmed': return 'Confirmé';
      case 'completed': return 'Terminé';
      case 'cancelled': return 'Annulé';
      default: return status;
    }
  };

  return (
    <div className="p-6">
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 mb-2">Secrétariat</h1>
          <p className="text-gray-600">Gérez vos rendez-vous et plannings</p>
        </div>
        <button
          onClick={() => setShowAddModal(true)}
          className="flex items-center space-x-2 px-4 py-2 bg-[#72C02C] text-white rounded-lg hover:bg-[#5da021] transition-colors"
        >
          <Plus className="w-4 h-4" />
          <span>Nouveau rendez-vous</span>
        </button>
      </div>

      {/* Filters */}
      <div className="mb-6">
        <div className="flex items-center space-x-2 bg-white rounded-lg p-4 shadow-sm border border-gray-200">
          <span className="text-sm font-medium text-gray-700">Filtrer par statut:</span>
          <select
            value={selectedFilter}
            onChange={(e) => setSelectedFilter(e.target.value)}
            className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#72C02C] focus:border-transparent"
          >
            <option value="all">Tous</option>
            <option value="scheduled">Programmé</option>
            <option value="confirmed">Confirmé</option>
            <option value="completed">Terminé</option>
            <option value="cancelled">Annulé</option>
          </select>
        </div>
      </div>

      {/* Appointments List */}
      <div className="space-y-4">
        {filteredAppointments.map((appointment) => (
          <div
            key={appointment.id}
            className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow"
          >
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center space-x-3 mb-2">
                  <h3 className="text-lg font-semibold text-gray-900">{appointment.title}</h3>
                  <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(appointment.status)}`}>
                    {getStatusLabel(appointment.status)}
                  </span>
                </div>
                
                <div className="flex items-center space-x-4 text-sm text-gray-500 mb-3">
                  <div className="flex items-center space-x-1">
                    <User className="w-4 h-4" />
                    <span>{appointment.client}</span>
                  </div>
                  <div className="flex items-center space-x-1">
                    <Calendar className="w-4 h-4" />
                    <span>{new Date(appointment.date).toLocaleDateString('fr-FR')}</span>
                  </div>
                  <div className="flex items-center space-x-1">
                    <Clock className="w-4 h-4" />
                    <span>{appointment.time} ({appointment.duration}min)</span>
                  </div>
                </div>
                
                {appointment.notes && (
                  <p className="text-sm text-gray-600 mb-3">{appointment.notes}</p>
                )}
                
                <div className="flex items-center space-x-2">
                  {appointment.status === 'scheduled' && (
                    <>
                      <button className="flex items-center space-x-1 px-3 py-1 bg-green-100 text-green-800 rounded-lg hover:bg-green-200 transition-colors">
                        <Check className="w-3 h-3" />
                        <span className="text-xs">Confirmer</span>
                      </button>
                      <button className="flex items-center space-x-1 px-3 py-1 bg-red-100 text-red-800 rounded-lg hover:bg-red-200 transition-colors">
                        <X className="w-3 h-3" />
                        <span className="text-xs">Annuler</span>
                      </button>
                    </>
                  )}
                  <button className="flex items-center space-x-1 px-3 py-1 bg-blue-100 text-blue-800 rounded-lg hover:bg-blue-200 transition-colors">
                    <Phone className="w-3 h-3" />
                    <span className="text-xs">Appeler</span>
                  </button>
                  <button className="flex items-center space-x-1 px-3 py-1 bg-gray-100 text-gray-800 rounded-lg hover:bg-gray-200 transition-colors">
                    <Mail className="w-3 h-3" />
                    <span className="text-xs">Email</span>
                  </button>
                </div>
              </div>
              
              <div className="flex items-center space-x-2 ml-4">
                <button className="p-2 text-[#72C02C] hover:text-[#5da021] transition-colors">
                  <Edit className="w-4 h-4" />
                </button>
                <button className="p-2 text-red-600 hover:text-red-800 transition-colors">
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Add Appointment Modal */}
      {showAddModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-xl shadow-lg w-full max-w-md">
            <div className="p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Nouveau rendez-vous</h3>
              <form className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Titre
                  </label>
                  <input
                    type="text"
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#72C02C] focus:border-transparent"
                    placeholder="Objet du rendez-vous"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Client
                  </label>
                  <input
                    type="text"
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#72C02C] focus:border-transparent"
                    placeholder="Nom du client"
                  />
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Date
                    </label>
                    <input
                      type="date"
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#72C02C] focus:border-transparent"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Heure
                    </label>
                    <input
                      type="time"
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#72C02C] focus:border-transparent"
                    />
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Durée (minutes)
                  </label>
                  <select className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#72C02C] focus:border-transparent">
                    <option value="30">30 minutes</option>
                    <option value="45">45 minutes</option>
                    <option value="60">1 heure</option>
                    <option value="90">1h30</option>
                    <option value="120">2 heures</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Notes
                  </label>
                  <textarea
                    rows={3}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#72C02C] focus:border-transparent"
                    placeholder="Notes additionnelles..."
                  />
                </div>
                <div className="flex space-x-3 pt-4">
                  <button
                    type="button"
                    onClick={() => setShowAddModal(false)}
                    className="flex-1 px-4 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors"
                  >
                    Annuler
                  </button>
                  <button
                    type="submit"
                    className="flex-1 px-4 py-2 text-white bg-[#72C02C] rounded-lg hover:bg-[#5da021] transition-colors"
                  >
                    Créer
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AppointmentsList;