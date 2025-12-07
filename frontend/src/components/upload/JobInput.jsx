import { useState } from 'react';

const JobInput = ({ onJobChange, jobData }) => {
  const [title, setTitle] = useState(jobData?.title || '');
  const [company, setCompany] = useState(jobData?.company || '');
  const [description, setDescription] = useState(jobData?.raw_text || '');

  const handleTitleChange = (e) => {
    setTitle(e.target.value);
    onJobChange({ title: e.target.value, company, raw_text: description });
  };

  const handleCompanyChange = (e) => {
    setCompany(e.target.value);
    onJobChange({ title, company: e.target.value, raw_text: description });
  };

  const handleDescriptionChange = (e) => {
    setDescription(e.target.value);
    onJobChange({ title, company, raw_text: e.target.value });
  };

  const handleClear = () => {
    setTitle('');
    setCompany('');
    setDescription('');
    onJobChange({ title: '', company: '', raw_text: '' });
  };

  return (
    <div className="w-full space-y-4">
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Job Title (Optional)
        </label>
        <input
          type="text"
          value={title}
          onChange={handleTitleChange}
          placeholder="e.g., Software Engineer"
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Company (Optional)
        </label>
        <input
          type="text"
          value={company}
          onChange={handleCompanyChange}
          placeholder="e.g., Google"
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      <div>
        <div className="flex justify-between items-center mb-2">
          <label className="block text-sm font-medium text-gray-700">
            Job Description
          </label>
          <div className="flex items-center space-x-2">
            <span className="text-xs text-gray-500">{description.length} characters</span>
            {description && (
              <button
                onClick={handleClear}
                className="text-xs text-red-500 hover:text-red-700"
              >
                Clear
              </button>
            )}
          </div>
        </div>
        <textarea
          value={description}
          onChange={handleDescriptionChange}
          placeholder="Paste the job description here..."
          rows={12}
          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
        />
      </div>
    </div>
  );
};

export default JobInput;

