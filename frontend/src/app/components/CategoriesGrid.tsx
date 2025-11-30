import Link from 'next/link'

async function getCategories() {
  const res = await fetch('http://localhost:8000/categories', {
    cache: 'no-store' // Ensure fresh data on each request
  })
  if (!res.ok) {
    throw new Error('Failed to fetch categories')
  }
  return res.json()
}

export default async function CategoriesGrid() {
  const categoriesData = await getCategories()

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8 py-8">
      {categoriesData.categories.map((category: string) => (
        <Link
          key={category}
          href={`/category/${encodeURIComponent(category)}`}
          className="bg-lightbg rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 p-8 block border border-borderlight transform hover:-translate-y-1"
        >
          <div className="text-center">
            <h3 className="text-2xl font-serif text-charcoal mb-3">{category}</h3>
            <p className="text-gray-600 text-lg mb-4">Explore our exquisite {category.toLowerCase()} collection</p>
            <div className="mt-4">
              <span className="inline-flex items-center px-6 py-2 rounded-full text-base font-medium bg-gold text-white hover:bg-gold-700 transition-colors duration-300 transform hover:scale-105">
                View Collection →
              </span>
            </div>
          </div>
        </Link>
      ))}
    </div>
  )
}
