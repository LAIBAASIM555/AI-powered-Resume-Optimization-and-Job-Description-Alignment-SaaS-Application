import { Star, Quote } from 'lucide-react';

const CustomerReviews = () => {
  const reviews = [
    {
      name: "Sarah Johnson",
      role: "Software Engineer",
      company: "Tech Corp",
      rating: 5,
      review: "This tool completely transformed my resume! I went from getting rejected by ATS systems to landing interviews at top tech companies. The recommendations were spot-on.",
      avatar: "SJ"
    },
    {
      name: "Michael Chen",
      role: "Marketing Manager",
      company: "Global Brands Inc",
      rating: 5,
      review: "Incredibly accurate skill matching and keyword optimization. My ATS score went from 65% to 92% after following the suggestions. Highly recommend!",
      avatar: "MC"
    },
    {
      name: "Emily Rodriguez",
      role: "Data Analyst",
      company: "Analytics Pro",
      rating: 5,
      review: "The detailed analysis and actionable recommendations helped me tailor my resume perfectly for each job application. Got 3x more interview calls!",
      avatar: "ER"
    },
    {
      name: "David Kim",
      role: "Product Manager",
      company: "InnovateTech",
      rating: 4,
      review: "Great tool for optimizing resumes. The skill gap analysis was particularly helpful in identifying what I needed to learn. Very user-friendly interface.",
      avatar: "DK"
    },
    {
      name: "Lisa Thompson",
      role: "UX Designer",
      company: "Design Studio",
      rating: 5,
      review: "As a designer, I was skeptical about AI tools, but this one impressed me. The format recommendations and keyword suggestions were exactly what I needed.",
      avatar: "LT"
    },
    {
      name: "James Wilson",
      role: "Financial Analyst",
      company: "Capital Group",
      rating: 5,
      review: "The ATS score improvement was dramatic. From struggling to get past initial screening to multiple offers. This tool is a game-changer for job seekers.",
      avatar: "JW"
    }
  ];

  const renderStars = (rating) => {
    return Array.from({ length: 5 }, (_, i) => (
      <Star
        key={i}
        className={`h-4 w-4 ${i < rating ? 'text-yellow-400 fill-current' : 'text-gray-300'}`}
      />
    ));
  };

  return (
    <section className="py-20 bg-gradient-to-br from-gray-50 to-blue-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">What Our Users Say</h2>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Join thousands of successful job seekers who have optimized their resumes with our AI-powered platform
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {reviews.map((review, index) => (
            <div
              key={index}
              className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow duration-300 animate-fade-in"
              style={{ animationDelay: `${index * 100}ms` }}
            >
              <div className="flex items-center mb-4">
                <div className="w-12 h-12 bg-primary-100 rounded-full flex items-center justify-center mr-4">
                  <span className="text-primary-600 font-semibold text-lg">{review.avatar}</span>
                </div>
                <div>
                  <h4 className="font-semibold text-gray-900">{review.name}</h4>
                  <p className="text-sm text-gray-600">{review.role} at {review.company}</p>
                </div>
              </div>

              <div className="flex items-center mb-4">
                {renderStars(review.rating)}
                <span className="ml-2 text-sm text-gray-600">({review.rating}/5)</span>
              </div>

              <div className="relative">
                <Quote className="h-8 w-8 text-primary-200 absolute -top-2 -left-2" />
                <p className="text-gray-700 italic pl-6">"{review.review}"</p>
              </div>
            </div>
          ))}
        </div>

        {/* Trust indicators */}
        <div className="mt-16 text-center">
          <div className="grid md:grid-cols-4 gap-8">
            <div className="bg-white rounded-lg p-6 shadow-md">
              <div className="text-3xl font-bold text-primary-600 mb-2">10,000+</div>
              <div className="text-gray-600">Happy Users</div>
            </div>
            <div className="bg-white rounded-lg p-6 shadow-md">
              <div className="text-3xl font-bold text-primary-600 mb-2">95%</div>
              <div className="text-gray-600">Success Rate</div>
            </div>
            <div className="bg-white rounded-lg p-6 shadow-md">
              <div className="text-3xl font-bold text-primary-600 mb-2">4.9/5</div>
              <div className="text-gray-600">Average Rating</div>
            </div>
            <div className="bg-white rounded-lg p-6 shadow-md">
              <div className="text-3xl font-bold text-primary-600 mb-2">24/7</div>
              <div className="text-gray-600">AI Support</div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default CustomerReviews;