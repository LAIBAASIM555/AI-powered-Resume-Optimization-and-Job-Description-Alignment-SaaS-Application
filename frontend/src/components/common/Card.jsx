const Card = ({ children, title, className = '' }) => {
  return (
    <div className={`bg-white rounded-xl shadow-md p-6 ${className}`}>
      {title && (
        <h3 className="text-xl font-semibold text-gray-800 mb-4">{title}</h3>
      )}
      {children}
    </div>
  );
};

export default Card;

