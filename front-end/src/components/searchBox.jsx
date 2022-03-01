import React, { Component } from "react";
import { getResult } from "../services/querySearch";
import Pagination from "./pagination";
import { paginate } from "../utils/paginate";

class SearchBox extends React.Component {
  state = {
    search: {
      searchquery: "",
    },
    data: {
      result: [],
      time: "",
    },
    pageSize: 20,
    currentPage: 1,
  };

  getPageDate = () => {
    const { currentPage, pageSize, data } = this.state;

    const result = paginate(data["result"], currentPage, pageSize);

    return { data: result };
  };

  handleChange = ({ currentTarget: input }) => {
    const search = { ...this.state.search };
    search[input.name] = input.value;
    this.setState({ search });
  };

  handlePageChange = (page) => {
    this.setState({ currentPage: page });
  };

  handleSearch = async () => {
    const data = await getResult(this.state.search.searchquery);
    this.setState({
      data: {
        result: data["data"]["result"],
        time: data["data"]["time"],
      },
    });
  };

  render() {
    const { time, result: allSearches } = this.state.data;
    const { data: result } = this.getPageDate();
    return (
      <div>
        <div className="input-group mb-3 my-3 ">
          <button
            style={{
              borderTopLeftRadius: "1rem",
              borderBottomLeftRadius: "1rem",
            }}
            className="btn btn-outline-primary"
            type="button"
            id="button-addon1"
            onClick={() => this.handleSearch()}
          >
            Search
          </button>
          <input
            style={{
              direction: "rtl",
            }}
            type="text"
            name="searchquery"
            className="form-control"
            placeholder="در انتظار جستجوی شما..."
            value={this.state.search.searchquery}
            onChange={(e) => this.handleChange(e)}
          />
        </div>
        <div style={{ direction: "rtl", marginRight: "20px" }}>
          {time && (
            <p>
              تعداد{" "}
              <span style={{ color: "red", fontWeight: "bold" }}>
                {allSearches.length}
              </span>{" "}
              جستجو در مدت زمان{" "}
              <span style={{ color: "red", fontWeight: "bold" }}>{time}</span>{" "}
              ثانیه
            </p>
          )}
          {result.map((tuple) => (
            <div key={tuple.id}>
              <a style={{ textDecoration: "none" }} href={tuple.url}>
                {tuple.title}
              </a>
              <p>{tuple.body.slice(400, 600)}</p>
            </div>
          ))}
        </div>
        <Pagination
          pageSize={this.state.pageSize}
          itemsCount={allSearches.length}
          onPageChange={this.handlePageChange}
          currentPage={this.state.currentPage}
        />
      </div>
    );
  }
}

export default SearchBox;
