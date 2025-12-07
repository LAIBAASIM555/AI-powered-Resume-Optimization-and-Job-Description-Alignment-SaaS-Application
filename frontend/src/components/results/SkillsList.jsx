const SkillsList = ({ matched, missing }) => {
  return (
    <div className="grid md:grid-cols-2 gap-6">
      {/* Matched Skills */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-800">Matched Skills</h3>
          <span className="bg-green-100 text-green-800 text-sm font-medium px-3 py-1 rounded-full">
            {matched?.length || 0}
          </span>
        </div>
        <div className="space-y-2">
          {matched && matched.length > 0 ? (
            matched.map((skill, index) => (
              <div
                key={index}
                className="flex items-center space-x-2 bg-green-50 border border-green-200 rounded-lg px-3 py-2"
              >
                <svg className="h-5 w-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
                <span className="text-sm text-gray-700">{skill}</span>
              </div>
            ))
          ) : (
            <p className="text-sm text-gray-500">No matched skills</p>
          )}
        </div>
      </div>

      {/* Missing Skills */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-800">Missing Skills</h3>
          <span className="bg-red-100 text-red-800 text-sm font-medium px-3 py-1 rounded-full">
            {missing?.length || 0}
          </span>
        </div>
        <div className="space-y-2">
          {missing && missing.length > 0 ? (
            missing.map((skill, index) => (
              <div
                key={index}
                className="flex items-center space-x-2 bg-red-50 border border-red-200 rounded-lg px-3 py-2"
              >
                <svg className="h-5 w-5 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
                <span className="text-sm text-gray-700">{skill}</span>
              </div>
            ))
          ) : (
            <p className="text-sm text-gray-500">No missing skills</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default SkillsList;

