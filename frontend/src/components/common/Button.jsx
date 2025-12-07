const Button = ({ 
  children, 
  variant = 'primary', 
  size = 'md', 
  loading = false, 
  disabled = false, 
  className = '',
  ...props 
}) => {
  const baseStyles = 'font-medium rounded-lg transition-all duration-200 flex items-center justify-center';
  
  const variants = {
    primary: 'bg-blue-600 text-white hover:bg-blue-700 shadow-md',
    secondary: 'bg-white text-blue-600 border border-blue-600 hover:bg-blue-50',
    danger: 'bg-red-500 text-white hover:bg-red-600',
  };
  
  const sizes = {
    sm: 'px-4 py-2 text-sm',
    md: 'px-6 py-3 text-base',
    lg: 'px-8 py-4 text-lg',
  };
  
  return (
    <button
      className={`${baseStyles} ${variants[variant]} ${sizes[size]} ${disabled ? 'opacity-50 cursor-not-allowed' : ''} ${className}`}
      disabled={disabled || loading}
      {...props}
    >
      {loading ? (
        <>
          <svg className="animate-spin h-5 w-5 mr-2" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
          </svg>
          Processing...
        </>
      ) : children}
    </button>
  );
};

export default Button;

