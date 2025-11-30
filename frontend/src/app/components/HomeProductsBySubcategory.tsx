import Link from 'next/link'
import Image from 'next/image'

interface Product {
  _id: string
  title: string
  description: string
  images: string[]
  category: string
  subcategory: string
  url: string
  details?: Record<string, any>
}

interface SubcategoryGroup {
  subcategory: string
  category: string
  products: Product[]
}

async function getProductsBySubcategory(): Promise<SubcategoryGroup[]> {
  const res = await fetch('http://localhost:8000/home/products-by-subcategory', {
    cache: 'no-store'
  })
  if (!res.ok) {
    throw new Error('Failed to fetch products')
  }
  const data = await res.json()
  return data.subcategories
}

export default async function HomeProductsBySubcategory() {
  const subcategoryGroups = await getProductsBySubcategory()

  return (
    <div className="space-y-16">
      {subcategoryGroups.map((group) => (
        <div key={group.subcategory} className="space-y-6">
          <div className="flex items-center justify-between border-b-2 border-gold pb-4">
            <div>
              <h2 className="text-3xl font-serif text-charcoal mb-2">{group.subcategory}</h2>
              <p className="text-gray-600 font-sans text-sm uppercase tracking-wider">{group.category}</p>
            </div>
            <Link
              href={`/category/${encodeURIComponent(group.category)}`}
              className="text-gold hover:text-gold-700 font-medium text-sm uppercase tracking-wider transition-colors duration-200"
            >
              View All →
            </Link>
          </div>
          
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {group.products.map((product) => (
              <Link
                key={product._id}
                href={`/product/${product._id}`}
                className="group bg-white rounded-lg shadow-md hover:shadow-2xl transition-all duration-300 overflow-hidden border border-borderlight transform hover:-translate-y-2"
              >
                <div className="relative h-72 bg-gradient-to-br from-gray-50 to-gray-100 overflow-hidden">
                  {product.images && product.images.length > 0 ? (
                    <Image
                      src={`http://localhost:8000/images/${product.images[0]}`}
                      alt={product.title}
                      fill
                      className="object-contain p-4 group-hover:scale-110 transition-transform duration-500"
                      sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 25vw"
                    />
                  ) : (
                    <div className="flex items-center justify-center h-full">
                      <span className="text-gray-400 font-serif">No Image</span>
                    </div>
                  )}
                  <div className="absolute inset-0 bg-gradient-to-t from-black/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                </div>
                <div className="p-5">
                  <h3 className="font-serif text-lg text-charcoal mb-2 line-clamp-2 group-hover:text-gold transition-colors duration-200">
                    {product.title}
                  </h3>
                  <p className="text-gray-600 text-sm line-clamp-2 mb-3">
                    {product.description.substring(0, 80)}...
                  </p>
                  <div className="flex items-center justify-between">
                    <span className="text-xs text-gray-500 uppercase tracking-wider">
                      {product.category}
                    </span>
                    <span className="text-gold text-sm font-medium">View Details →</span>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        </div>
      ))}
    </div>
  )
}

