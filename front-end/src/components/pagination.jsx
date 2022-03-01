import React from "react";
import _ from "lodash";

const Pagination = (props) => {
  const { pageSize, itemsCount, onPageChange, currentPage } = props;
  const pagesCount = Math.ceil(itemsCount / pageSize);
  console.log(pagesCount);
  if (pagesCount === 1 || pagesCount === 0) return null;
  const pages = _.range(1, 4);

  return (
    <nav
      style={{ display: "flex", justifyContent: "center" }}
      aria-label="Page navigation example"
    >
      <ul className="pagination">
        <li className="page-item">
          <a
            className="page-link"
            href="#"
            onClick={() =>
              onPageChange(currentPage === 1 ? pagesCount : currentPage - 1)
            }
          >
            Previous
          </a>
        </li>
        {pages.map((page) => (
          <li
            key={page}
            className={page === currentPage ? "page-item active" : "page-item"}
          >
            <a
              onClick={() => onPageChange(page)}
              className="page-link"
              href="#/"
            >
              {page}
            </a>
          </li>
        ))}
        <li className="page-item">
          <a
            className="page-link"
            href="#"
            onClick={() =>
              onPageChange(currentPage === pagesCount ? 1 : currentPage + 1)
            }
          >
            Next
          </a>
        </li>
      </ul>
    </nav>
  );
};

export default Pagination;
