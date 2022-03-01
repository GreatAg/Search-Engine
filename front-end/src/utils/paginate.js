import _ from "lodash";

export function paginate(items, PageNumber, PageSize) {
  const startIndex = (PageNumber - 1) * PageSize;
  return _(items).slice(startIndex).take(PageSize).value();
}
