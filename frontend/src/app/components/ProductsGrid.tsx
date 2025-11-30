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

async function getProductsByCategory(category: string): Promise<Product[]> {
  const res = await fetch(`http://localhost:8000/categories/${encodeURIComponent(category)}/products`, {
    cache: 'no-store'
  })
  if (!res.ok) {
    throw new Error('Failed to fetch products')
  }
  const data = await res.json()
  return data.products
}

export default async function ProductsGrid({ category }: { category: string }) {
  const products = await getProductsByCategory(category)

  if (products.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500 text-lg">No products found in this category.</p>
      </div>
    )
  }

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8 py-8">
      {products.map((product) => (
        <Link
          key={product._id}
          href={`/product/${product._id}`}
          className="bg-lightbg rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 overflow-hidden block border border-borderlight transform hover:-translate-y-1"
        >
          <div className="relative h-64 bg-darkbg overflow-hidden flex items-center justify-center">
            {product.images && product.images.length > 0 ? (
              <Image
                src={`http://localhost:8000/images/${product.images[0]}`}
                alt={product.title}
                fill
                className="object-contain transition-transform duration-300 hover:scale-105"
                sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 25vw"
              />
            ) : (
              <span className="text-gray-500 font-serif text-lg">No Image</span>
            )}
          </div>
          <div className="p-6">
            <h3 className="font-serif text-xl text-charcoal mb-2 line-clamp-2">
              {product.title}
            </h3>
            <p className="text-gray-600 text-sm line-clamp-3 mb-4">
              {product.description.substring(0, 100)}...
            </p>
            <div className="mt-3">
              <span className="inline-flex items-center px-4 py-2 rounded-full text-sm font-medium bg-gold text-white hover:bg-gold-700 transition-colors duration-300 shadow-lg">
                View Details →
              </span>
            </div>
          </div>
        </Link>
      ))}
    </div>
  )
}
