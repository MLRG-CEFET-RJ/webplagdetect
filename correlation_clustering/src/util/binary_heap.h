#include <iostream>
#include <vector>
#include <memory>
#include <math.h>

#ifndef BINARY_HEAP_H_
#define BINARY_HEAP_H_

namespace util{

template<class T, class Comparator>
class BinaryHeap{
 private:
    using index = std::size_t;
    using element_type = T;
 public:
    using comparator_type = Comparator;
    using heap_element_type = struct {
        element_type elem;
        index pos; // element position at heap
    };
 private:
    using heap_list_type = std::vector<heap_element_type*>;

    heap_list_type heap_;

    pair<index, index> get_children(index parent){
        index c1 = parent*2+1;
        index c2 = parent*2+2;
        return make_pair(c1, c2);
    }

    index get_parent_index(index child){
        if(child>=heap_.size())
            return -1;
        index parent = static_cast<index>(floor((child-1)/2.0));
        return parent;
    }

    void swap(index id1, index id2){
        std::swap(heap_[id1], heap_[id2]);
        std::swap(heap_[id1]->pos, heap_[id2]->pos);
    }

    void adjust_bottom_up(const index start, const comparator_type &comparator){
        index current = start;
        index parent = get_parent_index(current);
        while(parent < size()){
            if(comparator(heap_[current]->elem, heap_[parent]->elem)){
                swap(current, parent);
            }else
                break;
            current = parent;
            parent = get_parent_index(current);
        }
    }

    void adjust_top_down(const index start, const comparator_type &comparator){
        index current = start;
        while(current<size()){
            pair<index, index> children = get_children(current);
            index best = children.first;
            if(children.first < size()){
                if(children.second < size() && 
                   comparator(heap_[children.second]->elem, heap_[children.first]->elem)){
                    best = children.second;
                }

                if(comparator(heap_[best]->elem, heap_[current]->elem)){
                    swap(best, current);                
                }else
                    break;
            }
            current = best;
        }
    }

    void push_heap(heap_element_type *heap_elem,const comparator_type &comparator){
        heap_elem->pos = size();
        heap_.push_back(heap_elem);
        adjust_bottom_up(size() - 1, comparator);
    }

 public:
    BinaryHeap(){

    }

    void update(const index &pos, const comparator_type &comparator){
        adjust_bottom_up(pos, comparator);
        adjust_top_down(pos, comparator);
    }

    heap_element_type* push(const element_type &elem,const comparator_type &comparator){
        heap_element_type *heap_elem = new heap_element_type();
        heap_elem->elem = elem;
        push_heap(heap_elem, comparator);
        /*heap_elem->elem = elem;
        heap_elem->pos = size();
        heap_.push_back(heap_elem);
        adjust_bottom_up(size() - 1, comparator);
        */


        /*std::cout << "heap: ";
        for(heap_element_type *e: heap_){
            std::cout <<  e->elem << "[" << e->pos <<"] ";
        }
        std::cout << std::endl;
        getchar();*/
        return heap_elem;
    }

    void pop(const comparator_type &comparator){
        swap(0, size()-1);
        delete heap_[size()-1];
        heap_.pop_back();
        if (!heap_.empty())
            adjust_top_down(0, comparator);

        /*std::cout << "heap: ";
        for(heap_element_type *e: heap_){
            std::cout <<  e->elem << "[" << e->pos <<"] ";
        }
        std::cout << std::endl;
        getchar();*/
    }

    element_type pop_kth(int64_t k, const comparator_type &comparator) {
        std::vector<heap_element_type*> backup;
        for(int64_t i = 0; i < k; ++i) {
            backup.push_back(heap_[0]);
            swap(0, size() - 1);
            heap_.pop_back();
            adjust_top_down(0, comparator);
        }
        element_type element = top();
        pop(comparator);

        for(heap_element_type* heap_elem : backup) {
            push_heap(heap_elem, comparator);
        }

        return element;
    }

    bool empty() const{
        return heap_.empty();
    }

    element_type top() const{
        return heap_[0]->elem;
    }

    index size() const{
        return heap_.size();
    }

    void clear() {
        heap_.clear();
    }
};

}

#endif // BINARY_HEAP_H_
