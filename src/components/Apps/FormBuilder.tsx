import React, { useState } from 'react';
import { Plus, Eye, Edit, Trash2, FileText, Settings, Save } from 'lucide-react';

interface FormField {
  id: string;
  type: 'text' | 'email' | 'select' | 'checkbox' | 'textarea';
  label: string;
  required: boolean;
  options?: string[];
}

interface Form {
  id: string;
  name: string;
  description: string;
  fields: FormField[];
  createdAt: string;
  submissions: number;
}

const FormBuilder: React.FC = () => {
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [editingForm, setEditingForm] = useState<Form | null>(null);
  const [formFields, setFormFields] = useState<FormField[]>([]);
  const [formName, setFormName] = useState('');
  const [formDescription, setFormDescription] = useState('');

  const mockForms: Form[] = [
    {
      id: '1',
      name: 'Inscription événement',
      description: 'Formulaire d\'inscription pour les événements',
      fields: [
        { id: '1', type: 'text', label: 'Nom complet', required: true },
        { id: '2', type: 'email', label: 'Email', required: true },
        { id: '3', type: 'select', label: 'Département', required: true, options: ['Marketing', 'IT', 'RH'] }
      ],
      createdAt: '2024-01-15',
      submissions: 24
    },
    {
      id: '2',
      name: 'Feedback satisfaction',
      description: 'Formulaire de retour d\'expérience',
      fields: [
        { id: '1', type: 'text', label: 'Nom', required: false },
        { id: '2', type: 'textarea', label: 'Commentaires', required: true },
        { id: '3', type: 'checkbox', label: 'Je recommande', required: false }
      ],
      createdAt: '2024-01-20',
      submissions: 12
    }
  ];

  const addField = (type: FormField['type']) => {
    const newField: FormField = {
      id: Date.now().toString(),
      type,
      label: `Nouveau champ ${type}`,
      required: false,
      options: type === 'select' ? ['Option 1', 'Option 2'] : undefined
    };
    setFormFields([...formFields, newField]);
  };

  const updateField = (id: string, updates: Partial<FormField>) => {
    setFormFields(formFields.map(field => 
      field.id === id ? { ...field, ...updates } : field
    ));
  };

  const removeField = (id: string) => {
    setFormFields(formFields.filter(field => field.id !== id));
  };

  const getFieldTypeLabel = (type: string) => {
    switch (type) {
      case 'text': return 'Texte';
      case 'email': return 'Email';
      case 'select': return 'Liste déroulante';
      case 'checkbox': return 'Case à cocher';
      case 'textarea': return 'Zone de texte';
      default: return type;
    }
  };

  return (
    <div className="p-6">
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 mb-2">Formulaires</h1>
          <p className="text-gray-600">Créez et gérez vos formulaires personnalisés</p>
        </div>
        <button
          onClick={() => setShowCreateModal(true)}
          className="flex items-center space-x-2 px-4 py-2 bg-[#72C02C] text-white rounded-lg hover:bg-[#5da021] transition-colors"
        >
          <Plus className="w-4 h-4" />
          <span>Créer un formulaire</span>
        </button>
      </div>

      {/* Forms List */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {mockForms.map((form) => (
          <div
            key={form.id}
            className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow"
          >
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 bg-[#72C02C] bg-opacity-10 rounded-lg flex items-center justify-center">
                  <FileText className="w-5 h-5 text-[#72C02C]" />
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-gray-900">{form.name}</h3>
                  <p className="text-sm text-gray-500">{form.fields.length} champs</p>
                </div>
              </div>
              <div className="flex items-center space-x-1">
                <button className="p-1 text-gray-400 hover:text-gray-600 transition-colors">
                  <Eye className="w-4 h-4" />
                </button>
                <button className="p-1 text-[#72C02C] hover:text-[#5da021] transition-colors">
                  <Edit className="w-4 h-4" />
                </button>
                <button className="p-1 text-red-600 hover:text-red-800 transition-colors">
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            </div>
            
            <p className="text-gray-600 text-sm mb-4">{form.description}</p>
            
            <div className="flex items-center justify-between text-sm">
              <span className="text-gray-500">
                {form.submissions} soumissions
              </span>
              <span className="text-gray-500">
                {new Date(form.createdAt).toLocaleDateString('fr-FR')}
              </span>
            </div>
          </div>
        ))}
      </div>

      {/* Create/Edit Form Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-xl shadow-lg w-full max-w-4xl max-h-[90vh] overflow-y-auto">
            <div className="p-6">
              <div className="flex items-center justify-between mb-6">
                <h3 className="text-lg font-semibold text-gray-900">
                  Créer un formulaire
                </h3>
                <button
                  onClick={() => setShowCreateModal(false)}
                  className="text-gray-400 hover:text-gray-600"
                >
                  ×
                </button>
              </div>

              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Form Builder */}
                <div>
                  <div className="mb-6">
                    <h4 className="text-md font-semibold text-gray-900 mb-4">Configuration</h4>
                    <div className="space-y-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Nom du formulaire
                        </label>
                        <input
                          type="text"
                          value={formName}
                          onChange={(e) => setFormName(e.target.value)}
                          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#72C02C] focus:border-transparent"
                          placeholder="Nom du formulaire"
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Description
                        </label>
                        <textarea
                          value={formDescription}
                          onChange={(e) => setFormDescription(e.target.value)}
                          rows={3}
                          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#72C02C] focus:border-transparent"
                          placeholder="Description du formulaire"
                        />
                      </div>
                    </div>
                  </div>

                  <div className="mb-6">
                    <h4 className="text-md font-semibold text-gray-900 mb-4">Ajouter des champs</h4>
                    <div className="grid grid-cols-2 gap-2">
                      {[
                        { type: 'text', label: 'Texte' },
                        { type: 'email', label: 'Email' },
                        { type: 'select', label: 'Liste' },
                        { type: 'checkbox', label: 'Case' },
                        { type: 'textarea', label: 'Zone de texte' }
                      ].map(fieldType => (
                        <button
                          key={fieldType.type}
                          onClick={() => addField(fieldType.type as FormField['type'])}
                          className="p-2 text-sm bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
                        >
                          {fieldType.label}
                        </button>
                      ))}
                    </div>
                  </div>

                  <div>
                    <h4 className="text-md font-semibold text-gray-900 mb-4">Champs du formulaire</h4>
                    <div className="space-y-3">
                      {formFields.map((field) => (
                        <div key={field.id} className="border border-gray-200 rounded-lg p-3">
                          <div className="flex items-center justify-between mb-2">
                            <span className="text-sm font-medium text-gray-700">
                              {getFieldTypeLabel(field.type)}
                            </span>
                            <button
                              onClick={() => removeField(field.id)}
                              className="text-red-600 hover:text-red-800"
                            >
                              <Trash2 className="w-4 h-4" />
                            </button>
                          </div>
                          <input
                            type="text"
                            value={field.label}
                            onChange={(e) => updateField(field.id, { label: e.target.value })}
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#72C02C] focus:border-transparent mb-2"
                            placeholder="Libellé du champ"
                          />
                          <label className="flex items-center space-x-2">
                            <input
                              type="checkbox"
                              checked={field.required}
                              onChange={(e) => updateField(field.id, { required: e.target.checked })}
                              className="rounded border-gray-300 text-[#72C02C] focus:ring-[#72C02C]"
                            />
                            <span className="text-sm text-gray-600">Champ requis</span>
                          </label>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>

                {/* Preview */}
                <div>
                  <h4 className="text-md font-semibold text-gray-900 mb-4">Aperçu</h4>
                  <div className="bg-gray-50 rounded-lg p-4 min-h-[400px]">
                    <div className="bg-white rounded-lg p-6">
                      <h5 className="text-lg font-semibold text-gray-900 mb-2">
                        {formName || 'Nouveau formulaire'}
                      </h5>
                      <p className="text-gray-600 text-sm mb-6">
                        {formDescription || 'Description du formulaire'}
                      </p>
                      
                      <div className="space-y-4">
                        {formFields.map((field) => (
                          <div key={field.id}>
                            <label className="block text-sm font-medium text-gray-700 mb-1">
                              {field.label}
                              {field.required && <span className="text-red-500">*</span>}
                            </label>
                            {field.type === 'text' && (
                              <input
                                type="text"
                                className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                                disabled
                              />
                            )}
                            {field.type === 'email' && (
                              <input
                                type="email"
                                className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                                disabled
                              />
                            )}
                            {field.type === 'select' && (
                              <select className="w-full px-3 py-2 border border-gray-300 rounded-lg" disabled>
                                <option>Sélectionnez une option</option>
                              </select>
                            )}
                            {field.type === 'checkbox' && (
                              <label className="flex items-center space-x-2">
                                <input type="checkbox" className="rounded border-gray-300" disabled />
                                <span className="text-sm text-gray-600">Option</span>
                              </label>
                            )}
                            {field.type === 'textarea' && (
                              <textarea
                                rows={3}
                                className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                                disabled
                              />
                            )}
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div className="flex justify-end space-x-3 mt-6 pt-6 border-t">
                <button
                  onClick={() => setShowCreateModal(false)}
                  className="px-4 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors"
                >
                  Annuler
                </button>
                <button className="flex items-center space-x-2 px-4 py-2 bg-[#72C02C] text-white rounded-lg hover:bg-[#5da021] transition-colors">
                  <Save className="w-4 h-4" />
                  <span>Enregistrer</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default FormBuilder;