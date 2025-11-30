'use client';
import Link from 'next/link'
import Image from 'next/image'
import { useState, useEffect } from 'react';

interface Product {
  _id: string
  title: string
  description: string
  image: string
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

async function getProductsBySubcategory(page: number, size: number): Promise<SubcategoryGroup[]> {
  const res = await fetch(`http://localhost:8000/products?page=${page}&size=${size}`, {
    cache: 'no-store'
  });

  if (!res.ok) {
    throw new Error('Failed to fetch products');
  }

  const data = await res.json();

  // Debugging: Log the API response to understand its structure
  console.log('API Response:', data);

  // Ensure the response has a `products` property and it's an array
  if (!data || !data.data || !Array.isArray(data.data)) {
    console.error('Unexpected API response format:', data);
    throw new Error('Invalid API response format');
  }

  // Group products by subcategory
  const groupedProducts: Record<string, SubcategoryGroup> = {};
  data.data.forEach((product: Product) => {
    if (!groupedProducts[product.subcategory]) {
      groupedProducts[product.subcategory] = {
        subcategory: product.subcategory,
        category: product.category,
        products: []
      };
    }
    groupedProducts[product.subcategory].products.push(product);
  });

  return Object.values(groupedProducts);
}


export default function HomeProductsBySubcategory() {
  const [subcategoryGroups, setSubcategoryGroups] = useState<SubcategoryGroup[]>([]);
  const [page, setPage] = useState(1);
  const size = 20; // Number of products per page
  const [isLoading, setIsLoading] = useState(false);
  const [totalPages, setTotalPages] = useState(1); // Total number of pages

  useEffect(() => {
    const fetchProducts = async () => {
      setIsLoading(true);
      try {
        const res = await fetch(`http://localhost:8000/products?page=${page}&size=${size}`, {
          cache: 'no-store'
        });

        if (!res.ok) {
          throw new Error('Failed to fetch products');
        }

        const data = await res.json();

        // Extract metadata from the API response
        const { page: currentPage, total_pages: totalPagesFromApi } = data;
        setPage(currentPage || 1); // Update the current page
        setTotalPages(totalPagesFromApi || 1); // Update the total pages

        const groups = await getProductsBySubcategory(currentPage || 1, size);
        setSubcategoryGroups(groups);
      } catch (error) {
        console.error('Error fetching products:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchProducts();
  }, [page]);

  const handleNextPage = () => setPage((prev) => prev + 1);
  const handlePreviousPage = () => setPage((prev) => Math.max(prev - 1, 1));
  const handlePageClick = (pageNumber: number) => setPage(pageNumber);

  const renderPageNumbers = () => {
    const pages = [];
    const windowSize = 2;

    if (totalPages <= 1) return pages;

    // Always show the first page
    pages.push(
      <button
        key={1}
        onClick={() => handlePageClick(1)}
        className={`px-4 py-2 rounded ${
          page === 1 ? 'bg-gold text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
        }`}
      >
        1
      </button>
    );

    // Add ellipsis if there is a gap between the first page and the window
    if (page > windowSize + 2) {
      pages.push(
        <span key="start-ellipsis" className="px-2 text-gray-500">
          ...
        </span>
      );
    }

    // Add pages within the window around the current page
    for (let i = Math.max(2, page - windowSize); i <= Math.min(totalPages - 1, page + windowSize); i++) {
      pages.push(
        <button
          key={i}
          onClick={() => handlePageClick(i)}
          className={`px-4 py-2 rounded ${
            page === i ? 'bg-gold text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
          }`}
        >
          {i}
        </button>
      );
    }

    // Add ellipsis if there is a gap between the window and the last page
    if (page < totalPages - windowSize - 1) {
      pages.push(
        <span key="end-ellipsis" className="px-2 text-gray-500">
          ...
        </span>
      );
    }

    // Always show the last page
    pages.push(
      <button
        key={totalPages}
        onClick={() => handlePageClick(totalPages)}
        className={`px-4 py-2 rounded ${
          page === totalPages ? 'bg-gold text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
        }`}
      >
        {totalPages}
      </button>
    );

    return pages;
  };

  return (
    <div className="space-y-16">
      {isLoading ? (
        <p>Loading...</p>
      ) : (
        subcategoryGroups.map((group) => (
          <div key={group.subcategory} className="space-y-6">
            <div className="flex items-center justify-between border-b-2 border-gold pb-4">
              <div>
                <h2 className="text-3xl font-serif text-charcoal mb-2">{group.subcategory}</h2>
                <p className="text-gray-600 font-sans text-sm uppercase tracking-wider">{group.category}</p>
              </div>
            
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
              {group.products.map((product) => (
                <Link
                  key={product.id}
                  href={`/product/${product.id}`}
                  className="group bg-white rounded-lg shadow-md hover:shadow-2xl transition-all duration-300 overflow-hidden border border-borderlight transform hover:-translate-y-2"
                >
                  <div className="relative h-72 bg-gradient-to-br from-gray-50 to-gray-100 overflow-hidden">
                    {product.image ? (
                      <Image
                        src={`images/${product.image}`}
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
        ))
      )}

      <div className="flex justify-center space-x-4 mt-8">
        <button
          onClick={handlePreviousPage}
          disabled={page === 1}
          className="px-4 py-2 bg-gray-200 text-gray-700 rounded hover:bg-gray-300 disabled:opacity-50"
        >
          Previous
        </button>
        {renderPageNumbers()}
        <button
          onClick={handleNextPage}
          disabled={page === totalPages}
          className="px-4 py-2 bg-gray-200 text-gray-700 rounded hover:bg-gray-300 disabled:opacity-50"
        >
          Next
        </button>
      </div>
    </div>
  );
}